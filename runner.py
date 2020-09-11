from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from getdata import settings
from getdata.spiders.te import TeSpider
from getdata.spiders.te_adds import TeCurSpider
from getdata.spiders.cian import CianSpider
from getdata.spiders.irn import IRNSpider
from getdata.spiders.news import NewsSpider
from pymongo import MongoClient
import shutil
import os
import schedule
import time


# sudo docker run -p 8050:8050 scrapinghub/splash
# os.system('docker run -it --rm ubuntu bash')
def run():
    print(time.localtime())
    # очищаем базу данных перед обновлением
    if os.path.isdir('./images'):
        shutil.rmtree('images')
    client = MongoClient('localhost', 27017)
    mongo_base = client.db
    try:
        collections = [mongo_base['macro'],
                       mongo_base['cur'],
                       mongo_base['indexes'],
                       mongo_base['commodities'],
                       mongo_base['gov_bonds'],
                       mongo_base['irn'],
                       mongo_base['news'],
                       mongo_base['cian'],
                       mongo_base['stocks']]
        for collection in collections:
            collection.drop()
    except Exception as e:
        print(e)

    # запускаем скрапинг
    settings_m = Settings()
    settings_m.setmodule(settings)
    process = CrawlerProcess(settings=settings_m)
    # process.crawl(TeSpider)
    process.crawl(TeCurSpider)
    # process.crawl(CianSpider)
    process.crawl(IRNSpider)
    process.crawl(NewsSpider)
    process.start()


if __name__ == '__main__':
    schedule.every(15).minutes.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
