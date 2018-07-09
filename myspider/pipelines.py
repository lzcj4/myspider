from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


class AutoImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = "/".join([strip(item['char_index']),strip(item['brand_name']), strip(item['category_name']),
                           strip(item['car_name'] + "_" + item['price'])])
        feature="无"
        if request.url in item["image_urls"]:
            feature=item['features'][item["image_urls"].index(request.url)]
        filename = "{0}/{1}.jpg".format(folder, feature)
        return filename

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for img_url in item['image_urls']:
            referer = item['ref_url']
            yield Request(img_url, meta={'item': item, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path


if __name__ == "__main__":
    a = '我是一个？\*|“<>:/错误的字符串'
    print(strip(a))
