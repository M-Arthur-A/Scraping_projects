import scrapy
from scrapy.http import HtmlResponse
from getdata.items import GetdataItem
from copy import deepcopy


# from scrapy_splash import SplashRequest

class TeCurSpider(scrapy.Spider):
    name = 'te_adds'
    allowed_domains = ['tradingeconomics.com']
    start_urls = ['https://tradingeconomics.com/stocks', 'https://tradingeconomics.com/currencies',
                  'https://tradingeconomics.com/commodities', 'https://tradingeconomics.com/bonds']

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(
    #             url=url,
    #             callback=self.parse,
    #             endpoint='render.html',
    #             args={"wait": 2}
    #         )

    def parse(self, response: HtmlResponse):
        table_rows = response.xpath('//div[@class="table-responsive"]//tr')

        if response.url == 'https://tradingeconomics.com/currencies':
            for tr in table_rows:
                td = tr.xpath('.//td//text()').extract()
                if td:
                    item = GetdataItem(
                        cur_name=td[4],
                        cur_price=td[7],
                        cur_delta_now=td[9],
                        cur_delta_day=td[10],
                        cur_delta_week=td[11],
                        cur_delta_month=td[12],
                        cur_delta_year=td[13],
                        cur_data_date=td[14]
                    )
                    yield item

        if response.url == 'https://tradingeconomics.com/stocks':
            for tr in table_rows:
                td = tr.xpath('.//td//text()').extract()
                if td:
                    href = tr.xpath('.//td/a/@href').extract_first()
                    yield response.follow(href,
                                          callback=self.parse_stocks,
                                          meta={'attrs': deepcopy(td[4])})
                    item = GetdataItem(
                        index_name=td[4],
                        index_price=td[7],
                        index_delta_now=td[9],
                        index_delta_day=td[10],
                        index_delta_week=td[11],
                        index_delta_month=td[12],
                        index_delta_year=td[13],
                        index_data_date=td[14]
                    )
                    yield item

        if response.url == 'https://tradingeconomics.com/commodities':
            for tr in table_rows:
                td = tr.xpath('.//td//text()').extract()
                if td:
                    item = GetdataItem(
                        commodities_name=td[3] + ' (' + td[6] + ')',
                        commodities_price=td[8],
                        commodities_delta_now=td[10],
                        commodities_delta_day=td[11],
                        commodities_delta_week=td[12],
                        commodities_delta_month=td[13],
                        commodities_delta_year=td[14],
                        commodities_data_date=td[15]
                    )
                    yield item

        if response.url == 'https://tradingeconomics.com/bonds':
            for tr in table_rows:
                td = tr.xpath('.//td//text()').extract()
                if td:
                    item = GetdataItem(
                        bonds_name=td[4],
                        bonds_price=td[7],
                        bonds_delta_now=td[9],
                        bonds_delta_day=td[10],
                        bonds_delta_week=td[11],
                        bonds_delta_month=td[12],
                        bonds_delta_year=td[13],
                        bonds_data_date=td[14]
                    )
                    yield item

    def parse_stocks(self, response: HtmlResponse):
        table_rows = response.xpath('//div[@class="table-minimize"]//tr')
        for tr in table_rows:
            td = tr.xpath('.//td//text()').extract()
            if td:
                item = GetdataItem(
                    stocks_ticker=td[2],
                    stocks_name=td[6],
                    stocks_price=td[8],
                    stocks_delta_now=td[11],
                    stocks_delta_day=td[12],
                    stocks_delta_year=td[13],
                    stocks_data_date=td[14]
                )
                yield item
