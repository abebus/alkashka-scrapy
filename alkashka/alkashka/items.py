# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import time
from typing import TypedDict

from pydantic import BaseModel, Field


class PriceData(TypedDict):
    current: float
    original: float
    sale_tag: str


class Stock(TypedDict):
    in_stock: bool
    count: int


class Assets(TypedDict):
    main_image: str
    set_images: list[str]
    view360: list[str]
    video: list[str]


class Metadata(TypedDict, total=False):
    description: str


class AlkashkaItem(BaseModel):
    timestamp: int = Field(default_factory=lambda: int(time.time()))
    RPC: str
    url: str
    title: str
    marketing_tags: list[str]
    brand: str
    section: list[str]
    price_data: PriceData
    stock: Stock
    assets: Assets
    metadata: Metadata
    variants: int
