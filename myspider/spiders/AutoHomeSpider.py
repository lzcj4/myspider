import sys

sys.path.append("..")

import scrapy
import urllib
from myspider.items import AutoFeatureItem


class DmozSpider(scrapy.Spider):
    name = "autohome"
    allowed_domains = ["autohome.com.cn"]
    start_urls = [
        "https://www.autohome.com.cn/hangzhou/",
        # "https://www.autohome.com.cn/4427/#pvareaid=2023892"
    ]

    def __init__(self):
        self.domain = "https://www.autohome.com.cn"

    def parse(self, response):
        car_list = response.xpath("//div[@class=\"box\"]/p[1]/a")
        for car in car_list:
            car_url = self.domain + car.xpath("@href").extract()[0]
            if car_url is not None:
                yield scrapy.Request(car_url, callback=self.parse_item)

    def parse_item(self, response):
        car_name = response.xpath("//div[@class=\"subnav-title-name\"]/a/h1/text()").extract()[0]
        img_list = response.xpath("//ul[@class=\"carpic-list fn-clear\"][position()<3]/li/a[1]")
        for img in img_list:
            auto_item = AutoFeatureItem()
            auto_item["car_name"] = car_name
            auto_item["feature"] = img.xpath(".//img/@alt").extract()[0]
            auto_item["ref_url"] = response.request.url

            auto_item["small_img_url"] = img.xpath(".//img/@data-original").extract()[0]
            big_img_url = "https:" + img.xpath("@href").extract()[0]
            auto_item["big_img_url"] = big_img_url
            auto_item['image_urls'] = auto_item["small_img_url"]
            yield auto_item
