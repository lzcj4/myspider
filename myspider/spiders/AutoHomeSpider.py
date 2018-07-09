import sys
import string

sys.path.append("..")

import scrapy
import urllib
from myspider.items import AutoFeatureItem


class AutoHomeSpider(scrapy.Spider):
    name = "autohome"
    allowed_domains = ["autohome.com.cn"]
    start_urls = [
        "https://www.autohome.com.cn/car/",
        # "https://www.autohome.com.cn/4427/#pvareaid=2023892"
    ]

    def __init__(self):
        self.domain = "https://www.autohome.com.cn"

    def parse(self, response):
        # yield scrapy.Request("https://www.autohome.com.cn/grade/carhtml/{0}.html".format("G"),
        #                      callback=self.parse_car_brands, meta={"char_index": "G"})

        for c in string.ascii_uppercase:
            if c:
                yield scrapy.Request("https://www.autohome.com.cn/grade/carhtml/{0}.html".format(c),
                                     callback=self.parse_car_brands, meta={"char_index": c})

    def parse_car_brands(self, response):
        char_index = response.request.meta["char_index"]
        brands = response.xpath("//dl")
        for b in brands:
            brand_name = b.xpath(".//dt/div/a/text()").extract()[0]
            categories = b.xpath(".//div[@class=\"h3-tit\"]")

            for c in categories:
                i = 0
                category_name = c.xpath(".//a/text()").extract()[0]
                autos = c.xpath("following-sibling::ul/li")
                for a in autos:
                    i += 1
                    auto_item = AutoFeatureItem()
                    auto_item["char_index"] = char_index
                    auto_item["brand_name"] = brand_name
                    auto_item["category_name"] = category_name
                    car_info = a.xpath(".//a/text()").extract()
                    if not car_info:
                        continue
                    auto_item["car_name"] = car_info[0]
                    auto_item["price"] = "(指导价：{0})".format(car_info[1]) \
                        if car_info[1] not in ("图库", "报价") else "(指导价：暂无)"
                    auto_item["features"] = []
                    car_url = "https:" + a.xpath(".//a[1]/@href").extract()[0]
                    print("{}、{}_{}_{}".format(i, brand_name, category_name, car_info[0], car_info[1]))
                    yield scrapy.Request(car_url, callback=self.parse_item, meta={"item": auto_item})

    def parse_item(self, response):
        img_list = response.xpath("//ul[@class=\"carpic-list fn-clear\"][position()<3]/li/a[1]")
        auto_item = response.request.meta["item"]
        print("{}、{}_{}_{}".format(auto_item["brand_name"], auto_item["category_name"],
                                   auto_item["car_name"], response.request.url))
        i = 1
        if img_list:
            for img in img_list:
                f = img.xpath(".//img/@alt").extract()[0]
                if f in auto_item["features"]:
                    auto_item["features"].append("{0}_{1}".format(f, i))
                    i += 1
                else:
                    auto_item["features"].append(f)
                auto_item["ref_url"] = response.request.url
                auto_item['image_urls'] = []
                auto_item["small_img_url"] = img.xpath(".//img/@data-original").extract()[0]
                big_img_url = "https:" + img.xpath("@href").extract()[0]
                auto_item["big_img_url"] = big_img_url
                yield scrapy.Request(big_img_url, callback=self.parse_big_img_item, meta={"item": auto_item})
        else:
            img_list = response.xpath("//ul[@class=\"piclist\"]/li")
            if img_list:
                for img in img_list:
                    f = img.xpath(".//p/a/text()").extract()[0]
                    if f in auto_item["features"]:
                        auto_item["features"].append("{0}_{1}".format(f, i))
                        i += 1
                    else:
                        auto_item["features"].append(f)
                    auto_item["ref_url"] = response.request.url
                    auto_item['image_urls'] = []
                    auto_item["small_img_url"] = img.xpath(".//img/@src").extract()[0]
                    big_img_url = "https:" + img.xpath(".//a/@href").extract()[0]
                    auto_item["big_img_url"] = big_img_url
                    yield scrapy.Request(big_img_url, callback=self.parse_big_img_item, meta={"item": auto_item})
            else:
                img_list = response.xpath("//dl[@class=\"models_pics\"]")
                if img_list:
                    for img in img_list:
                        auto_item["ref_url"] = response.request.url
                        auto_item['image_urls'] = img.xpath(".//img/@src").extract()
                        for i in range(len(auto_item['image_urls'])):
                            auto_item["features"].append("{0}_{1}".format("全图", i))

                        auto_item["small_img_url"] = img.xpath(".//img/@src").extract()[0]
                        yield auto_item
                else:
                    pass

    def parse_big_img_item(self, response):
        item = response.request.meta['item']
        img_url = response.xpath("//div[@class=\"pic\"]/img/@src").extract()[0]
        if img_url:
            item['image_urls'].append("https:" + img_url)
            yield item
        else:
            pass
