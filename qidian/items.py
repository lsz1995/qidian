# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class QidianItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    author = Field()
    introduce = Field()
    yuepiao = Field()
    dashang = Field()

class xiaoshuoItem(Item):
    id = Field()
    title = Field()
    chapter = Field()
    info= Field()

