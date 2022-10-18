import scrapy
# from scrapy_playwright_demo.items import QuoteItem
from scrapy_selenium import SeleniumRequest


class JSQuotesSpider(scrapy.Spider):
    name = 'jsquotes'
    #scrapy crawl jsquotes -O jsquotes.json

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        # yield scrapy.Request(url, meta={'playwright': True})
        yield SeleniumRequest(url=url, callback=self.parse)


    # def parse(self, response):
    #     quote_item = QuoteItem()
    #     for quote in response.css('div.quote'):
    #         quote_item['text'] = quote.css('span.text::text').get()
    #         quote_item['author'] = quote.css('small.author::text').get()
    #         quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
    #         yield quote_item

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.ant-pagination-item-active + li a::attr(href)').get()
        if next_page is not None and "page=3" not in next_page:
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, callback=self.parse)