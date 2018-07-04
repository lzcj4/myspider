# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoFeatureItem(scrapy.Item):
    '''车型信息'''
    car_name = scrapy.Field()
    feature = scrapy.Field()
    small_img_url = scrapy.Field()
    big_img_url = scrapy.Field()

    image_urls = scrapy.Field()
    ref_url = scrapy.Field()
    images = scrapy.Field()
