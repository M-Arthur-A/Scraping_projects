import scrapy
from scrapy.http import HtmlResponse
from getdata.items import GetdataItem
from copy import deepcopy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['kommersant.ru']
    start_urls = ['https://www.kommersant.ru/rubric/3', 'https://www.kommersant.ru/finance']

    def parse(self, response: HtmlResponse):
        if response.url == 'https://www.kommersant.ru/rubric/3':
            rubric = 'economics'
        else:
            rubric = 'finance'
        topics = response.xpath(
            '//div[@class="grid_cell grid_cell_big js-middle"]//h4[contains(@class, "uho")]/a//text()').extract()
        resumes = response.xpath(
            '//div[@class="grid_cell grid_cell_big js-middle"]//h3[contains(@class, "uho")]/a//text()').extract()
        hrefs = response.xpath(
            '//div[@class="grid_cell grid_cell_big js-middle"]//h3[contains(@class, "uho")]/a/@href').extract()
        for i, href in enumerate(hrefs):
            variable = {'rubric': rubric, 'topic': topics[i], 'resume': resumes[i], 'href': href}
            yield response.follow(href,
                                  callback=self.get_item,
                                  meta={'attrs': deepcopy(variable)})

    def get_item(self, response: HtmlResponse):
        text = response.xpath(
            '//div[@class="article_text_wrapper"]//*[local-name()="div" or local-name()="p" and not(contains(@class, "b_incut"))]//text()').extract()
        variables = response.meta['attrs']
        variables['text'] = text
        yield GetdataItem(news_variables=variables)
