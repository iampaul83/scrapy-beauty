import scrapy

# QuotesSpider subclasses scrapy.Spider
class QuotesSpider(scrapy.Spider):

    """
    identifies the Spider. It must be unique within a project,
    that is, you can’t set the same name for different Spiders.
    """
    name = "quotes"

    """
    must return an iterable of Requests (you can return a list of requests or write a generator function)
    which the Spider will begin to crawl from.
    Subsequent requests will be generated successively from these initial requests.
    """
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    """
    a method that will be called to handle the response downloaded for each of the requests made.
    The response parameter is an instance of TextResponse that holds the page content
    and has further helpful methods to handle it.
    """
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }