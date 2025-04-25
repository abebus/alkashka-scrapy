from __future__ import annotations

from typing import Any
from uuid import UUID

from typing_extensions import List, NotRequired, TypedDict, Union

# Cities


class CityResponse(TypedDict):
    success: bool
    meta: Meta
    results: List[AccentedOrResult]


class Meta(TypedDict("FromFieldMixin", {"from": int}), TypedDict):
    to: int
    per_page: int
    current_page: int
    has_more_pages: bool
    accented: List[AccentedOrResult]


class AccentedOrResult(TypedDict):
    uuid: UUID
    name: str
    slug: str
    longitude: str
    latitude: str
    accented: bool


# Products


class ProductResponse(TypedDict):
    success: bool
    meta: Meta
    results: List[ProductResult]


class ProductMeta(TypedDict("FromFieldMixin", {"from": int}), TypedDict):
    to: int
    per_page: int
    current_page: int
    has_more_pages: bool
    total: int
    facets: List[ProductFacet]
    sorts: ProductSorts


class ProductFacet(TypedDict):
    code: str
    title: str
    type: str
    placeholder: Union[None, str]
    unit: str
    values: NotRequired[List[Any | ProductValue]]
    enabled: NotRequired[bool]
    min: NotRequired[float]
    max: NotRequired[float]


class ProductValue(TypedDict):
    slug: str
    name: str
    enabled: bool


class ProductSorts(TypedDict):
    recomended: str
    newest: str
    price_asc: str
    price_desc: str
    discount: str


class ProductResult(TypedDict):
    uuid: UUID
    name: str
    slug: str
    category_slug: str
    rate: None
    vendor_code: int
    subname: Union[None, str]
    new: bool
    recomended: bool
    price: int
    prev_price: int
    status: str
    quantity_total: int
    axioma: bool
    enogram: bool
    has_online_price: bool
    quantity: int
    favorite: bool
    image_url: str
    product_url: str
    action_labels: List[ProductActionLabel]
    filter_labels: List[ProductFilterLabel]
    available: bool
    warning: None
    category: ProductCategory


class ProductActionLabel(TypedDict):
    title: str
    color: str


class ProductFilterLabel(TypedDict):
    title: str
    filter: str
    type: str
    value: NotRequired[str]
    values: NotRequired[ProductValues]


class ProductValues(TypedDict):
    min: float
    max: float


class ProductCategory(TypedDict):
    uuid: UUID
    name: str
    background_color: str
    slug: str
    parent_uuid: UUID
    parent: ProductParent


class ProductParent(TypedDict):
    uuid: UUID
    name: str
    slug: str


# Product details


class ProductDetailResponse(TypedDict):
    success: bool
    results: ProductDetailResponseResults


class ProductDetailResponseResults(TypedDict):
    uuid: UUID
    vendor_code: int
    country_code: str
    country_name: str
    name: str
    new: bool
    enogram: bool
    axioma: bool
    gift_package: bool
    price: int
    prev_price: int
    quantity_total: int
    axioma_filter: None
    enogram_filter: None
    quantity: int
    favorite: bool
    offline_price: int
    image_url: str
    price_details: List[ProductDetailResponsePriceDetail]
    available: bool
    warning: None
    category: ProductDetailResponseCategory
    filter_labels: List[ProductDetailResponseFilterLabel]
    subname: str
    description_blocks: List[ProductDetailResponseDescriptionBlock]
    text_blocks: List[Any]
    availability_title: str
    availability: ProductDetailResponseAvailability
    gastronomics: List[Any]


class ProductDetailResponsePriceDetail(TypedDict):
    prev_price: int
    price: int
    title: str


class ProductDetailResponseCategory(TypedDict):
    uuid: UUID
    name: str
    parent_uuid: UUID
    background_color: str
    slug: str
    parent: ProductDetailResponseParent


class ProductDetailResponseParent(TypedDict):
    uuid: UUID
    name: str
    slug: str


class ProductDetailResponseFilterLabel(TypedDict):
    title: str
    filter: str
    type: str
    value: NotRequired[str]
    values: NotRequired[ProductDetailResponseValues]


class ProductDetailResponseValues(TypedDict):
    min: float
    max: float


class ProductDetailResponseDescriptionBlock(TypedDict):
    code: str
    title: str
    type: str
    placeholder: None
    unit: str
    values: NotRequired[List[ProductDetailResponseValue]]
    min: NotRequired[float]
    max: NotRequired[float]
    enabled: NotRequired[bool]


class ProductDetailResponseValue(TypedDict):
    slug: str
    name: str
    enabled: bool


class ProductDetailResponseAvailability(TypedDict):
    title: str
    stores: List[ProductDetailResponseStore]


class ProductDetailResponseStore(TypedDict):
    uuid: UUID
    title: str
    phone: str
    opening_hours: str
    longitude: str
    latitude: str
    price: int
    quantity: str
