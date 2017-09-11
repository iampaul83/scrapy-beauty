import scrapy

# QuotesSpider subclasses scrapy.Spider
class QuotesSpider(scrapy.Spider):
    name = "beauty"

    def start_requests(self):
        urls = [
            'https://www.ptt.cc/bbs/Beauty/index2269.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, cookies={'over18': 1}, callback=self.parse)

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for post_link in response.css('.r-ent'):
            link = post_link.css('.title > a')
            push = post_link.css('.nrec > span')
            # ignore deleted links
            if link.extract_first() is not None:
                link_data = {
                    'title': link.css('::text').extract_first(),
                    'url': 'https://www.ptt.cc' + link.css('::attr(href)').extract_first()
                }
                # add push data
                if push.extract_first():
                    link_data['push'] = {
                        'class': push.css("span::attr(class)").re_first(r'(f\d)'),
                        'num': push.css("span::text").extract_first()
                    }
                request = scrapy.Request(link_data['url'], callback=self.parse_page)
                request.meta['link_data'] = link_data
                yield request

    def parse_page(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        link_data = response.meta['link_data']
        link_data['images'] = response.css("#main-content > a::attr(href)").extract()
        [link_data['author'], _, link_data['date']] = response.css("#main-content > .article-metaline > .article-meta-value::text").extract()
        yield link_data
