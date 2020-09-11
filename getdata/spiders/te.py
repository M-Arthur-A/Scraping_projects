import scrapy
from scrapy.http import HtmlResponse
from getdata.items import GetdataItem
from scrapy_splash import SplashRequest

LUA_CLICK_BUTTON = '''
function main(splash)
    assert(splash:go(splash.args.url))
    local get_dimensions = splash:jsfunc([[
        function () {
            var rect = document.getElementById('ctl00_ContentPlaceHolder1_ctl04_LinkButton1').getClientRects()[0];
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


class TeSpider(scrapy.Spider):
    name = 'te'
    allowed_domains = ['tradingeconomics.com']
    start_urls = ['https://tradingeconomics.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={"wait": 2, 'lua_source': LUA_CLICK_BUTTON}
            )

    def parse(self, response: HtmlResponse):
        table_rows = response.xpath('//div[@id="homematrix"]//tr')
        dataset = []
        for tr in table_rows:
            td = tr.xpath('.//td')
            for t in td:
                cell = t.xpath('.//a/text()').extract()
                dataset.append(cell)
            if dataset:
                item = GetdataItem(
                    macro_country=dataset[0],
                    macro_gdp=dataset[1],
                    macro_gdp_yoy=dataset[2],
                    macro_gdp_qoq=dataset[3],
                    macro_interest=dataset[4],
                    macro_inflation=dataset[5],
                    macro_jobless=dataset[6],
                    macro_budget=dataset[7],
                    macro_debt_to_gdp=dataset[8],
                    macro_cur_acc=dataset[9],
                    macro_population=dataset[10]
                )
                dataset = []
                yield item
