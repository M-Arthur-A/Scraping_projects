import scrapy
from scrapy.http import HtmlResponse, JsonRequest
import json
from getdata.items import GetdataItem
from scrapy_splash import SplashRequest
from copy import deepcopy

LUA_CLICK_BUTTON = '''
function main(splash)
    assert(splash:go(splash.args.url))
    local get_dimensions = splash:jsfunc([[
        function () {
            var rect = document.getElementsByClassName('btn.btn_load_more').getClientRects()[0];
            return {"x": rect.left, "y": rect.top}
        }
    ]])
    splash:set_viewport_full()
    splash:wait(0.1)
    local dimensions = get_dimensions()
    splash:mouse_click(dimensions.x, dimensions.y)

    -- Wait split second to allow event to propagate.
    splash:wait(2)
    return splash:html()
end
'''
LUA_CLICK_BUTTON = '''
function main(splash, args)
    splash.private_mode_enabled = false
    assert(splash:go(args.url))
    btn = splash:select('button.btn.btn_load_more')
    btn:mouse_click()
    assert(splash:wait(2))
    return splash:html()
end
'''
LUA_CLICK_BUTTON = '''
function main(splash, args)
splash.private_mode_enabled = false
assert(splash:go(args.url))
for i = 1,splash.args.n do
    btn = splash:select('button.btn.btn_load_more')
    btn:mouse_click()          
    splash:wait(2)
return splash:html()
end
'''

class EfrsbSpider(scrapy.Spider):
    name = 'efrsb'
    allowed_domains = ['fedresurs.ru']
    start_urls = ['https://fedresurs.ru/']
    with open('./inn_list.txt', 'r') as f:
        inn_list = f.read().splitlines()

    def parse(self, response: HtmlResponse):
        for inn in self.inn_list:
            url = self.start_urls[0] + 'search/entity?code=' + inn
            yield SplashRequest(
                url=url,
                callback=self.parse_inn,
                args={"wait": 2},
                meta={'inn': deepcopy(inn)}
            )

    def parse_inn(self, response: HtmlResponse):
        next_url = response.xpath('//a[@class="td_company_name"]//@href').extract_first()
        name = response.xpath('//a[@class="td_company_name"]/text()').extract_first()
        method = 'splash'
        # method = 'POST'
        if method == 'POST':
            i = 0
            data = {"guid": str(next_url.split('/')[-1]),
                    "pageSize": '15',
                    "startRowIndex": str(i),
                    "searchAmReport": 'true', "searchFirmBankruptMessage": 'true',
                    "searchFirmBankruptMessageWithoutLegalCase": 'false', "searchSfactsMessage": 'true',
                    "searchSroAmMessage": 'true', "searchTradeOrgMessage": 'true', "sfactMessageType": 'null',
                    "sfactsMessageTypeGroupId": 'null'}
            headers = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3', 'Connection': 'keep-alive',
                       'Content-Length': '456', 'Content-Type': 'application/json',
                       'DNT': '1', 'Host': 'fedresurs.ru', #'Cookie': 'fedresurscookie=30c888cee5f1d2550f4fddd2236eaba9',
                       'Origin': 'https://fedresurs.ru',
                       'Referer': f'https://fedresurs.ru{next_url}', 'TE': 'Trailers',
                       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
            yield scrapy.Request('https://fedresurs.ru/backend/companies/publications',
                                 method='POST',
                                 body=json.dumps(data),
                                 callback=self.parse_actions,
                                 headers=headers,
                                 meta={'company_name': deepcopy(name),
                                       'inn': deepcopy(response.meta['inn'])})
        else:
            yield SplashRequest(
                url=self.start_urls[0] + next_url[1:],
                callback=self.parse_actions,
                args={"wait": 5},
                meta={'company_name': deepcopy(name),
                      'inn': deepcopy(response.meta['inn'])}
            )

    def parse_actions(self, response: HtmlResponse):
        itms = response.xpath('//span/span[@class="msgs_sum"]/text()').extract_first().split('(')[1].split(')')[0]
        n = itms//15 + 1 if itms%15 > 0 else itms//15
        if response.xpath('//button[@class="btn btn_load_more"]'):
            yield SplashRequest(
                url=response.url,
                callback=self.parse_actions,
                endpoint='execute',
                args={"wait": 2, 'lua_source': LUA_CLICK_BUTTON, 'n': n}
            )
        else:
            hrefs = list(zip(response.xpath('//h4/a/@href').extract(), response.xpath('//h4/a/text()').extract()))
            for href in hrefs:
                yield response.follow(href[0],
                                      callback=self.parse_action,
                                      meta={'company_name': deepcopy(response.meta['company_name']),
                                            'inn': deepcopy(response.meta['inn']),
                                            'action': deepcopy(href[1])})

    def parse_action(self, response: HtmlResponse):
        urls = response.xpath()
        for url in urls:
            yield response.follow(url, callback=self.get_item)

    def get_item(self, response: HtmlResponse):
        item = GetdataItem(
            # macro_country=dataset[0],
            # macro_gdp=dataset[1],
            # macro_gdp_yoy=dataset[2],
            # macro_gdp_qoq=dataset[3],
            # macro_interest=dataset[4],
            # macro_inflation=dataset[5],
            # macro_jobless=dataset[6],
            # macro_budget=dataset[7],
            # macro_debt_to_gdp=dataset[8],
            # macro_cur_acc=dataset[9],
            # macro_population=dataset[10]
        )
        yield item
