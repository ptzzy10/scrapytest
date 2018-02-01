'''
题目：范例虎丘网
描述：
'''
from scrapy import Request

from coolscrapy.items import HuxiuItem
import scrapy
global newsnum
class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = ["http://www.huxiu.com/index.php"]

    def parse(self, response):
        print('==============================parse')

        newsnum = 1
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
            print('==============================',newsnum)
            item = HuxiuItem()
            item['title'] = sel.xpath('h2/a/text()')[0].extract()
            item['link'] = sel.xpath('h2/a/@href')[0].extract()
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()
            url = response.urljoin(item['link'])
            print("标题：",item['title'])
            print("链接：", url)
            print("描述：", item['desc'])
            newsnum+=1
            if(newsnum==5):
                break
            yield Request(url,callback=self.parse_article)

    def parse_article(self,response):
        print('==============================parse_article： ')
        item = HuxiuItem()
        detail_div = response.xpath('//div[@class="article-wrap"]')
        item['title'] = detail_div.xpath('h1/text()').extract()
        item['link'] = response.url
        item['posttime'] = detail_div.xpath('div/div/span[@class="article-time pull-left"]/text()').extract()
        print("详细标题：", item['title'])
        print("详细链接：", item['link'])
        print("详细时间：", item['posttime'])
        yield item    #注意如果没有这句的话，pipelines.py中的process_item不会被调用

