from scrapy.spiders import CrawlSpider, Rule, XMLFeedSpider
from scrapy.linkextractors import LinkExtractor

from coolscrapy.items import HuxiuItem, XMLItem


#链接爬取蜘蛛，专门为那些爬取有特定规律的链接内容而准备的。
class XMLSpider(XMLFeedSpider):
    name = "xml"
    namespaces = [('atom', 'http://www.w3.org/2005/Atom')]
    allowed_domains = ["127.0.0.1"]
    start_urls = ["http://127.0.0.1/atom1.xml"]
    iterator = 'xml' #默认为iternodes。貌似对于有namespace的xml不行
    itertag = 'atom:entry'

    def parse_node(self, response, selector):
        item = XMLItem()
        item['title'] = response.xpath('atom:title/text()')[0].extract()
        item['link'] = response.xpath('atom:link/@href')[0].extract()
        item['id'] = response.xpath('atom:id/text()')[0].extract()
        item['published'] = response.xpath('atom:published/text()')[0].extract()
        item['updated'] = response.xpath('atom:updated/text()')[0].extract()
        item['content'] = response.xpath('atom:content/text()')[0].extract()
        print(item['title'], item['link'], item['id'])
        self.logger.info('[%s],[%s],[%s]', item['title'], item['link'], item['id'])
        yield item
    def parse_nodes(self, response, nodes):
        # self.logger.info('Hi, this is a <%s> node!', self.itertag)
        item = XMLItem()
        item['title'] = nodes.xpath('atom:title/text()')[0].extract()
        item['link'] = nodes.xpath('atom:link/@href')[0].extract()
        item['id'] = nodes.xpath('atom:id/text()')[0].extract()
        item['published'] = nodes.xpath('atom:published/text()')[0].extract()
        item['updated'] = nodes.xpath('atom:updated/text()')[0].extract()
        item['content'] = nodes.xpath('atom:content/text()')[0].extract()
        print(item['title'], item['link'], item['id'])
        self.logger.info('[%s],[%s],[%s]',item['title'], item['link'], item['id'])
        yield item
