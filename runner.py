from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from getdata import settings
from getdata.spiders.efrsb import EfrsbSpider
import shutil
import os
import time


# sudo docker run -p 8050:8050 scrapinghub/splash
# os.system('docker run -it --rm ubuntu bash')
def run():
    print(time.localtime())

    # запускаем скрапинг
    settings_m = Settings()
    settings_m.setmodule(settings)
    process = CrawlerProcess(settings=settings_m)
    process.crawl(EfrsbSpider)
    process.start()


if __name__ == '__main__':
    run()