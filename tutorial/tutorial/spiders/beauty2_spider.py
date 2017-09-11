import scrapy

# QuotesSpider subclasses scrapy.Spider
class QuotesSpider(scrapy.Spider):
    name = "beauty2"
    page_limit = 1
    page = 0
    post = 0

    def __init__(self, page_limit=1, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.page_limit = int(page_limit)

    def start_requests(self):
        urls = [
            'https://www.ptt.cc/bbs/Beauty/index.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, cookies={'over18': 1}, callback=self.parse)

    def parse(self, response):
        self.page += 1
        if self.page > self.page_limit:
            return

        prev_page_href = response.css('#action-bar-container .btn-group-paging > a:nth-child(2)::attr(href)').extract_first()
        if prev_page_href:
            yield scrapy.Request(url=response.urljoin(prev_page_href), cookies={'over18': 1}, callback=self.parse)

        for post_link in response.css('.r-ent'):
            link = post_link.css('.title > a')
            push = post_link.css('.nrec > span')
            # ignore deleted links
            if link.extract_first() is not None:
                link_data = {
                    'title': link.css('::text').extract_first(),
                    'url': response.urljoin(link.css('::attr(href)').extract_first())
                }
                # add push data
                if push.extract_first():
                    link_data['push'] = {
                        'class': push.css("span::attr(class)").re_first(r'(f\d)'),
                        'num': push.css("span::text").extract_first()
                    }
                request = scrapy.Request(link_data['url'], cookies={'over18': 1}, callback=self.parse_page)
                request.meta['link_data'] = link_data
                yield request

    def parse_page(self, response):
        # if self.post == 0:
        #     from scrapy.shell import inspect_response
        #     inspect_response(response, self)
        self.post += 1
        # log every 10 post
        if self.post % 10 == 0:
            self.logger.info('scraping %sth post', self.post)
        link_data = response.meta['link_data']
        link_data['images'] = response.css("#main-content > a::attr(href)").extract()
        link_data['meta'] = []
        # [link_data['author'], _, link_data['date']] = response.css("#main-content > .article-metaline > .article-meta-value::text").extract()
        for meta in response.css("#main-content > .article-metaline"):
            link_data['meta'].append({
                'tag': meta.css('.article-meta-tag::text').extract_first(),
                'value': meta.css('.article-meta-value::text').extract_first()
            })
        yield link_data
