import scrapy
from scrapy_selenium import SeleniumRequest

class LazadaSpider(scrapy.Spider):
    name = "lazada"
    #scrapy crawl lazada -O lazada.json
    # start_urls = [
    #     'https://shopee.co.th/%E0%B9%82%E0%B8%97%E0%B8%A3%E0%B8%A8%E0%B8%B1%E0%B8%9E%E0%B8%97%E0%B9%8C%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%96%E0%B8%B7%E0%B8%AD-cat.11044951.11045117?brands=1269140&page=0&sortBy=pop',
    # ]

    def start_requests(self):
        url = "https://www.lazada.co.th/shop-mobiles/"
        # yield scrapy.Request(url, callback=self.parse)
        # yield scrapy.Request(url, meta={'playwright': True})
        yield SeleniumRequest(
            url=url, 
            callback=self.parse, 
            wait_time=5,
            script="document.querySelector('li.ant-pagination-next>button').click()",
            )

    def parse(self, response):
        # with open('screenshot/image.png', 'wb') as image_file:
        #     image_file.write(response.meta['screenshot'])
        # for quote in response.css('div.uA1waf _4QQ4Ir'):
        #     yield {
        #         'text': quote.css('div.vc0PvV AxYdVM::text').get(),
        #         # 'author': quote.css('small.author::text').get(),
        #         # 'tags': quote.css('div.tags a.tag::text').getall(),
        #     }

        
        for quote in response.css('img::attr(alt)').getall():
            yield {
                'text': quote,
                # 'author': quote.css('small.author::text').get(),
                # 'tags': quote.css('div.tags a.tag::text').getall(),
            } 
        # next_page = response.css('li.next a::attr(href)').get()
        next_page = response.css('li.ant-pagination-item-active + li a::attr(href)').get()
        if next_page is not None and "page=3" not in next_page:
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, callback=self.parse)

    # def parse(self, response):
    #     # page = response.url.split("/")[-2]
    #     filename = f'lazada.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)