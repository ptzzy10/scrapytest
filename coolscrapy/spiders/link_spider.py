from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from coolscrapy.items import HuxiuItem, LinkItem

#链接爬取蜘蛛，专门为那些爬取有特定规律的链接内容而准备的。
class CrawlSpider(CrawlSpider):
    name = "crawl"
    allowed_domains = ["huxiu.com"]
    start_urls = ["http://www.huxiu.com/index.php"]

    rules = (
        # 提取匹配正则式'/group?f=index_group'链接 (但是不能匹配'deny.php')
        # 并且会递归爬取(如果没有定义callback，默认follow=True).
        Rule(LinkExtractor(allow=('/group?f=index_group',),deny=('deny\.php',))),
        # 提取匹配'/article/\d+/\d+.html'的链接，并使用parse_item来解析它们下载后的内容，不递归
        #Rule(LinkExtractor(allow=('/article/\d+/\d+\.html',)),callback='parse_item'),
        Rule(LinkExtractor(allow=('/article/\d+.html',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        detail = response.xpath('//div[@class="article-wrap"]')
        item = LinkItem()
        item['title'] = detail.xpath('h1/text()')[0].extract()
        item['link'] = response.url
        item['posttime'] = detail.xpath(
            'div[@class="article-author"]/div[@class="column-link-box"]/span[contains(@class,"article-time")]/text()')[0].extract()
        print(item['title'], item['link'], item['posttime'])
        yield item