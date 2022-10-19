import scrapy
from scrapy_selenium import SeleniumRequest

class JSQuotesSpider(scrapy.Spider):
    name = 'jsquotes'
    #scrapy crawl jsquotes -O jsquotes.json

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield SeleniumRequest(url=url, callback=self.parse)
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.ant-pagination-item-active + li a::attr(href)').get()
        if next_page is not None :
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, callback=self.parse)