# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BookItem(Item):
    """Book item"""
    url = Field()
    category = Field()
    title = Field()
    image = Field()
    rating = Field()
    description = Field()
    upc = Field()
    product_type = Field()
    price_excluding_tax = Field()
    price_including_tax = Field()
    tax = Field()
    availability = Field()
    number_of_reviews = Field()
