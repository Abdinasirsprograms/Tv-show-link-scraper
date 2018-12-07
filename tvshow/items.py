# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TvshowsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tv_Show = scrapy.Field()
    season = scrapy.Field()
    episode = scrapy.Field()
    number_Of_Links = scrapy.Field()
    links_404 = scrapy.Field()
    links_to_avoid = scrapy.Field()
    links = scrapy.Field()
    pass
