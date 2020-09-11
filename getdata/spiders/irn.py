import scrapy
from scrapy.http import HtmlResponse
from getdata.items import GetdataItem


class IRNSpider(scrapy.Spider):
    name = 'irn'
    allowed_domains = ['irn.ru']
    # start_urls = ['https://www.irn.ru/gd/?class=all&type=1&period=1&grnum=1&currency=0&select=period']
    start_urls = ['https://www.irn.ru/graph/services/classes2.php?class=all&type=1&period=1&grnum=1&currency=0']

    def parse(self, response: HtmlResponse):
        item = GetdataItem(
            irn_pic=response.body
        )
        yield item
