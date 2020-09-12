from itemadapter import ItemAdapter
from scrapy.http import HtmlResponse
from copy import deepcopy
import os


class GetdataPipeline:
    def process_item(self, item, spider):
        if spider.name == 'efrsb':
            item = self.clear_item(item, spider)
        return item

    def clear_item(self, item, spider):
        if spider.name == 'te' or spider.name == 'te_adds':
            for key in item.keys():
                if spider.name == 'te':
                    item[key] = item[key][0]
                item[key] = item[key].replace('\n', '').replace('\r', '')
                item[key] = ''.join(item[key].split('  ')).strip()
        return item
