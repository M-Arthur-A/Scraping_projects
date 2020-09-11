from itemadapter import ItemAdapter
from scrapy.http import HtmlResponse
from pymongo import MongoClient
from copy import deepcopy
import os


class GetdataPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.db

    def process_item(self, item, spider):
        if spider.name == 'te':
            collection = self.mongo_base['macro']
            item = self.clear_item(item, spider)
        elif spider.name == 'te_adds':
            if item.keys().__contains__('cur_name'):
                collection = self.mongo_base['cur']
                item = self.clear_item(item, spider)
            elif item.keys().__contains__('index_name'):
                collection = self.mongo_base['indexes']
                item = self.clear_item(item, spider)
            elif item.keys().__contains__('stocks_name'):
                collection = self.mongo_base['stocks']
                item = self.clear_item(item, spider)
            elif item.keys().__contains__('commodities_name'):
                collection = self.mongo_base['commodities']
                item = self.clear_item(item, spider)
            elif item.keys().__contains__('bonds_name'):
                collection = self.mongo_base['gov_bonds']
                item = self.clear_item(item, spider)
        elif spider.name == 'cian':
            file_path = f'./images/{item["cian_variables"]["dealType"]}/{item["cian_variables"]["category"]}/{item["cian_variables"]["region"]}.png'
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(file_path, 'wb') as f:
                f.write(item['cian_pic'])
            item['cian_variables']['pic_path'] = file_path
            del item['cian_pic']
            collection = self.mongo_base['cian']
        elif spider.name == 'irn':
            file_path = r'./images/irn/msk.png'
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(file_path, 'wb') as f:
                f.write(item['irn_pic'])
            item['irn_pic'] = file_path
            collection = self.mongo_base['irn']
        elif spider.name == 'news':
            item = self.clear_item(item, spider)
            item['news_rubric'] = item['news_variables']['rubric']
            item['news_topic'] = item['news_variables']['topic']
            item['news_resume'] = item['news_variables']['resume']
            item['news_href'] = item['news_variables']['href']
            item['news_text'] = item['news_variables']['text']
            del item['news_variables']
            collection = self.mongo_base['news']
        collection.insert_one(item)
        return item

    def clear_item(self, item, spider):
        if spider.name == 'te' or spider.name == 'te_adds':
            for key in item.keys():
                if spider.name == 'te':
                    item[key] = item[key][0]
                item[key] = item[key].replace('\n', '').replace('\r', '')
                item[key] = ''.join(item[key].split('  ')).strip()

        elif spider.name == 'news':
            text = []
            itm = ''
            if item['news_variables']['href'] == '/doc/4467706':
                print(1)
            item['news_variables']['topic'] = item['news_variables']['topic'].replace(u'\xa0', u' ')
            item['news_variables']['resume'] = item['news_variables']['resume'].replace(u'\xa0', u' ')
            item['news_variables']['href'] = 'https://www.kommersant.ru' + item['news_variables']['href']
            for txt in item['news_variables']['text']:
                itm = txt.replace(u'\xa0', u' ').replace('\xa0', ' ')
                itm = itm.replace('\r', '').replace('\t', '').replace('\n', '')
                if itm:
                    text.append(itm)
            text = '\n\n'.join(text)
            item['news_variables']['text'] = deepcopy(text)
        return item
