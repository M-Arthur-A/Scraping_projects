import scrapy
from scrapy.http import HtmlResponse
from getdata.items import GetdataItem
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
from copy import deepcopy

LUA_SAVE_PIC = '''
 -- Arguments:
 -- * url - URL to render;
 -- * css - CSS selector to render;
 -- * pad - screenshot padding size.

 -- this function adds padding around region
 function pad(r, pad)
 return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
 end

-- main script
function main(splash)

-- this function returns element bounding box
local get_bbox = splash:jsfunc([[
function(css) {
  var el = document.querySelector(css);
  var r = el.getBoundingClientRect();
  return [r.left, r.top, r.right, r.bottom];
}
]])

assert(splash:go(splash.args.url))
assert(splash:wait(0.5))

-- don't crop image by a viewport
splash:set_viewport_full()

local region = pad(get_bbox(splash.args.css), splash.args.pad)
return splash:png{region=region}
end
'''


class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['cian.ru']
    start_urls = ['https://www.cian.ru/analitika-nedvizhimosti-online/']

    regions = ['spb',  # Питер
               'lo',  # Ленинградская область
               'msk',  # Москва
               'mo',  # Московская область
               'other'  # Регионы
               ]
    deal_types = ['sale',  # продажа
                  'rent'  # аренда
                  ]
    categories_sale = ['suburbanSale',  # загородная
                       'newBuildingFlatSale',  # первичка
                       'flatSale'  # вторичка
                       ]
    categories_rent = ['flatRent',  # квартира длительная аренда
                       'suburbanRent'  # загородная
                       ]

    def start_requests(self):
        variables = {'dealType': 'sale', 'region': 'msk', 'category': 'newBuildingFlatSale'}
        for reg in self.regions:
            variables['region'] = reg
            for deal in self.deal_types:
                variables['dealType'] = deal
                if deal == 'sale':
                    categories = self.categories_sale
                else:
                    categories = self.categories_rent
                for category in categories:
                    variables['category'] = category
                    url = f'{self.start_urls[0]}?{urlencode(variables)}'
                    yield SplashRequest(
                        url=url,
                        callback=self.parse,
                        endpoint='execute',
                        args={"wait": 2,
                              'lua_source': LUA_SAVE_PIC,
                              'pad': 32,
                              'css': 'div._61cc05a7c9--container--2FebD'},
                        meta={'attrs': deepcopy(variables)}
                    )

    def parse(self, response: HtmlResponse):
        item = GetdataItem(
            cian_pic=response.body,
            cian_variables=response.meta['attrs']
        )
        yield item
