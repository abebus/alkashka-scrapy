from typing import Generator

import scrapy
from scrapy.http.response.json import JsonResponse

import alkashka.patch_orjson_as_json  # noqa Monkey patch json to orjson
from alkashka.items import AlkashkaItem, Assets, Metadata, PriceData, Stock

from .models import AccentedOrResult as CityResult
from .models import ProductDetailResponseResults

GET_CITIES_URL = "https://alkoteka.com/web-api/v1/city"
GET_PRODUCTS_URL = "https://alkoteka.com/web-api/v1/product"
DEFAULT_START_URLS = (
    "https://alkoteka.com/catalog/slaboalkogolnye-napitki-2",
    "https://alkoteka.com/catalog/krepkiy-alkogol",
    "https://alkoteka.com/catalog/vino",
)
DEFAULT_PER_PAGE = "200"


class AlkashkaSpider(scrapy.Spider):
    city_uuid: None | str = None
    city_name: None | str = None
    name = "alkashka_spider"

    def __init__(
        self,
        name: None | str = None,
        city: None | str = None,
        filename: None | str = None,
        urls: None | str = None,
        **kwargs,
    ):
        if not city:
            city = "Краснодар"
            # Fallback to Краснодар потому что в ТЗ
            # raise ValueError(f"Must specify a city to parse from.")

        self.city_name = city

        if not filename:
            try:
                with open("urls.txt") as f:
                    urls = f.readlines()
            except FileNotFoundError:
                self.logger.info("File with urls not found.")

        if urls:
            self.start_urls = urls.split(",")
        else:
            self.start_urls = DEFAULT_START_URLS

        if len(self.start_urls) < 3:
            raise ValueError("At least 3 urls must be provided")

        super().__init__(name, **kwargs)

    def start_requests(self) -> Generator[None, None, scrapy.Request]:
        yield scrapy.Request(GET_CITIES_URL, callback=self.parse_cities)

    def parse_cities(
        self, response: JsonResponse
    ) -> Generator[None, None, scrapy.Request]:
        for city in response.jmespath("results"):
            city_obj: CityResult = city.get()
            if city_obj["name"] == self.city_name:
                self.city_uuid = str(city_obj["uuid"])
                for url in self.start_urls:
                    yield scrapy.FormRequest(
                        GET_PRODUCTS_URL,
                        callback=self.parse_products_json,
                        formdata={
                            "city_uuid": self.city_uuid,
                            "root_category_slug": url.split("/")[-1],
                            "per_page": DEFAULT_PER_PAGE,
                            "page": "1",
                        },
                        method="GET",
                        meta={"per_page": DEFAULT_PER_PAGE, "page": "1"},
                    )
                return

        raise ValueError(f"City with name {self.city_name} can't be found")

    def parse_products_json(
        self, response: JsonResponse
    ) -> Generator[None, None, scrapy.Request]:
        # product.get(): ProductResult
        for product in response.jmespath("results"):
            yield scrapy.FormRequest(
                f"{GET_PRODUCTS_URL}/{product.jmespath('slug').get()}",
                formdata={"city_uuid": self.city_uuid},
                callback=self.parse_detail,
                method="GET",
                cb_kwargs={"product_url": product.jmespath("product_url").get()},
            )
        if response.jmespath("meta.has_more_pages").get():
            yield scrapy.FormRequest(
                GET_PRODUCTS_URL,
                callback=self.parse_products_json,
                formdata={
                    "city_uuid": self.city_uuid,
                    "per_page": DEFAULT_PER_PAGE,
                    "page": str(response.meta.get("page") + 1),
                },
                meta={
                    "per_page": DEFAULT_PER_PAGE,
                    "page": str(response.meta.get("page") + 1),
                },
                method="GET",
            )

    def parse_detail(
        self, response: JsonResponse, product_url: str
    ) -> Generator[None, None, AlkashkaItem]:
        product_jmespath = response.jmespath("results")
        product_dict: ProductDetailResponseResults = product_jmespath.get()
        yield AlkashkaItem(
            RPC=product_dict["uuid"],
            url=product_url,
            title=", ".join(
                [product_dict["name"]]
                + product_jmespath.jmespath("filter_labels.title").getall()
            ),
            marketing_tags=product_jmespath.jmespath("price_detail.title").getall(),
            brand=product_jmespath.jmespath(
                "description_blocks[?code == `proizvoditel`].title"
            ).get()
            or product_jmespath.jmespath(
                "description_blocks[?code == `brend`].values[0].name"
            ).get(),
            section=product_jmespath.jmespath(
                "[category.name, category.parent.name]"
            ).getall(),
            price_data=PriceData(
                current=product_dict["price"],
                original=product_dict["prev_price"],
                sale_tag=f"Скидка {int((product_dict['prev_price'] - product_dict['price']) / product_dict['prev_price'])}"
                if product_dict["price"] != product_dict["prev_price"]
                else "",
            ),
            stock=Stock(
                in_stock=product_dict["quantity_total"] > 0,
                count=product_dict["quantity_total"],
            ),
            assets=Assets(
                main_image=product_dict["image_url"],
                set_images=[""],  # not any?
                view360=[""],
                video=[""],
            ),
            metadata=Metadata(
                description="\n".join(
                    product_jmespath.jmespath(
                        """
                [
                    description_blocks[?unit != `null` && unit != ''].join(' ', [title, to_string(min), unit]),
                    description_blocks[?unit == `null` || unit == ''].join(': ', [title, values[0].name])
                ][] | [?@ != `null`]
                """
                    ).getall()
                ),
                subname=product_dict["subname"],
                vendor_code=product_dict["vendor_code"],
                contry_code=product_dict["country_code"],
                country_name=product_dict["country_name"],
                gastronimics=product_dict["gastronomics"],
            ),
            variants=1,
        )
