# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    Author = scrapy.Field()
    Desc = scrapy.Field()
    Year = scrapy.Field()
    Img = scrapy.Field()
    ISBN = scrapy.Field()
    Page = scrapy.Field()
    Genre = scrapy.Field()
    Tag = scrapy.Field()

    pass
