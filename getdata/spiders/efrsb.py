import scrapy
from scrapy.http import HtmlResponse
import json
from getdata.items import GetdataItem
from copy import deepcopy
from scrapy_splash import SplashRequest


class EfrsbSpider(scrapy.Spider):
    name = 'efrsb'
    allowed_domains = ['bankrot.fedresurs.ru', 'fedresurs.ru']
    start_urls = ['https://fedresurs.ru/']
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    with open('./inn_list.txt', 'r') as f:
        inn_list = f.read().splitlines()


    def parse(self, response: HtmlResponse):
        for inn in self.inn_list:
            url = 'https://fedresurs.ru/backend/companies/search'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                       'Referer': f'https://fedresurs.ru/search/entity?code={str(inn)}',
                       'Content-type': 'application/json', 'Host': 'fedresurs.ru', 'Origin': 'https://fedresurs.ru'}
            data = {"entitySearchFilter": {"startRowIndex": 0, "pageSize": 15, "code": str(inn), "onlyActive": False}}

            yield response.follow(
                url=url,
                method='POST',
                body=json.dumps(data),
                callback=self.parse_mes_list,
                headers=headers,
                meta={'inn': deepcopy(inn)})

    def parse_mes_list(self, response: HtmlResponse):
        inn_id = json.loads(response.text)['pageData'][0]['guid']
        url = 'https://fedresurs.ru/backend/companies/publications'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                   'Referer': f'https://fedresurs.ru/company/{inn_id}',
                   'Content-type': 'application/json', 'Host': 'fedresurs.ru', 'Origin': 'https://fedresurs.ru'}
        data = {"guid": inn_id, "pageSize": 15, "startRowIndex": 0,
                "searchAmReport": True, "searchFirmBankruptMessage": True,
                "searchFirmBankruptMessageWithoutLegalCase": False, "searchSfactsMessage": True,
                "searchSroAmMessage": True, "searchTradeOrgMessage": True}
        yield response.follow(url,
                              method='POST',
                              body=json.dumps(data),
                              callback=self.parse_mes_list_all,
                              headers=headers,
                              meta={'inn': deepcopy(response.meta['inn']), 'inn_id': deepcopy(inn_id)})

    def parse_mes_list_all(self, response: HtmlResponse):
        inn_id = response.meta['inn_id']
        url = 'https://fedresurs.ru/backend/companies/publications'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                   'Referer': f'https://fedresurs.ru/company/{inn_id}',
                   'Content-type': 'application/json', 'Host': 'fedresurs.ru', 'Origin': 'https://fedresurs.ru'}
        publications_count = json.loads(response.text)['found']
        i = 0
        for _ in range(publications_count // 15 + (1 if publications_count % 15 > 0 else 0)):
            data = {"guid": inn_id, "pageSize": 15, "startRowIndex": i,
                    "searchAmReport": True, "searchFirmBankruptMessage": True,
                    "searchFirmBankruptMessageWithoutLegalCase": False, "searchSfactsMessage": True,
                    "searchSroAmMessage": True, "searchTradeOrgMessage": True}
            yield response.follow(url,
                                  method='POST',
                                  body=json.dumps(data),
                                  callback=self.parse_action,
                                  headers=headers,
                                  meta={'inn': deepcopy(response.meta['inn']),
                                        'inn_id': deepcopy(response.meta['inn_id'])})
            i += 15

    def parse_action(self, response: HtmlResponse):
        for message in json.loads(response.text)['pageData']:
            guid = message['guid']
            mes_type = message['type']

            if mes_type == 'AmReport':  # итоговый отчет конкурсного
                url = 'https://bankrot.fedresurs.ru/AuReportCard.aspx?rid=' + guid
                yield response.follow(url, callback=self.get_item, meta={'inn': deepcopy(response.meta['inn']),
                                                                         'inn_id': deepcopy(response.meta['inn_id']),
                                                                         'message': deepcopy(message)})

            elif mes_type == 'BankruptcyMessage':  # обычное сообщение на старом домене
                url = 'https://bankrot.fedresurs.ru/MessageWindow.aspx?ID=' + guid
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                    'Referer': url,
                    'Accept': 'text/html', 'Host': 'bankrot.fedresurs.ru', 'Origin': 'https://fedresurs.ru',
                    'TE': 'Trailers', 'Cookie': 'bankrotcookie=f69a7cc51d1332ab11b30cf4038e572c'}
                # yield response.follow(url + '&attempt=1', callback=self.get_item,
                #                       headers=headers,
                #                       meta={'inn': deepcopy(response.meta['inn']),
                #                             'inn_id': deepcopy(response.meta['inn_id']),
                #                             'message': deepcopy(message)})
                yield SplashRequest(
                    url=url,
                    callback=self.get_item,
                    args={"wait": 2}, meta={'inn': deepcopy(response.meta['inn']),
                                            'inn_id': deepcopy(response.meta['inn_id']),
                                            'message': deepcopy(message)})

            elif mes_type == 'sfactmessage':
                url = 'https://fedresurs.ru/sfactmessage/' + guid
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                    'Referer': f'https://fedresurs.ru/company/{response.meta["inn_id"]}',
                    'Content-type': 'application/json', 'Host': 'fedresurs.ru', 'Origin': 'https://fedresurs.ru'}
                yield response.follow(url, callback=self.get_item, headers=headers,
                                      meta={'inn': deepcopy(response.meta['inn']),
                                            'inn_id': deepcopy(response.meta['inn_id']),
                                            'message': deepcopy(message)})
            else:
                print(message, 'НЕИЗВЕСТНЫЙ ТИП СООБЩЕНИЯ!!!')

    def get_item(self, response: HtmlResponse):

        print(response.meta)
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
