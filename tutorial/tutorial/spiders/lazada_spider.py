import scrapy
from scrapy_selenium import SeleniumRequest

class LazadaSpider(scrapy.Spider):
    name = "lazada"
    #scrapy crawl lazada -O lazada.json

    crawling = False    
    export_html = False

    def start_requests(self):
        start_urls = [
            'https://www.lazada.co.th/shop-mobiles/',
            "https://www.lazada.co.th/shop-mobiles/?page=21",
        ]
        # url = "https://www.lazada.co.th/shop-mobiles/?page=21"
        # yield scrapy.Request(url, callback=self.parse)
        # yield scrapy.Request(url, meta={'playwright': True})
        for url in start_urls :
            yield SeleniumRequest(
                url=url, 
                callback=self.parse, 
                # script="document.querySelector('li.ant-pagination-next>button').click()",
                )

    def parse(self, response):        
        for quote in response.css('img::attr(alt)').getall():
            yield {
                'text': quote,
                'url' : response.url,
                # 'author': quote.css('small.author::text').get(),
                # 'tags': quote.css('div.tags a.tag::text').getall(),
            } 
            
        if self.crawling :
            # next_page = response.css('li.next a::attr(href)').get()    
            next_page = response.css('li.ant-pagination-item-active + li a::attr(href)').get()
            # if next_page is not None and "page=5" not in next_page:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield SeleniumRequest(url=next_page, callback=self.parse)
        
        if self.export_html:
            # page = response.url.split("/")[-2]
            filename = f'lazada.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
    