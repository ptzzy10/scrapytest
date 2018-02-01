import scrapy
import requests
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from coolscrapy.items import HuxiuItem, LinkItem, NovelSortItem
import re
#链接爬取蜘蛛，专门为那些爬取有特定规律的链接内容而准备的。
class QuanshuSpider(scrapy.Spider):
    name = "quanshu"
    allowed_domains = ["quanshuwang.com"]
    start_urls = ["http://www.quanshuwang.com/index.html"]

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        '''
        result = response.text
        title_reg = r'<ul class="channel-nav-list">(.*?)</ul>'
        url_list = re.findall(title_reg, result)
        print(url_list)
        reg2 =r'<a href="(.*?)">(.*?)</a>'
        novel_url_list = re.findall(reg2, url_list)
        print(novel_url_list)
        #获取地址sdf 士大夫fsd f 士大夫 
'''

        fenlei_urls = response.xpath("//ul[@class='channel-nav-list']/li/a/@href").extract()
        fenlei_ming = response.xpath("//ul[@class='channel-nav-list']/li/a/text()").extract()
        item = NovelSortItem()
        item['sort_name'] = fenlei_ming
        item['sort_url'] = fenlei_urls
        yield  item
        self.logger.info('=========================')
        for url in fenlei_urls:
            yield Request(url, callback=self.parse_xiaoshuoming)

    def get_total_page_num(self,response):#获取某类小说总页数
        numall_str = response.xpath('//em[@id="pagestats"]/text()').extract()
        total_page_num = int((numall_str[0].split('/'))[1])
        self.logger.info('response.url = %s,tatal_page_num = %d' % (response.url, total_page_num))
        return total_page_num

    def get_xiaoshuo_mingzi_jianjieurl(self,response):
        reg = r'<a target="_blank" title="(.*?)" href="(.*?)" class="clearfix stitle">'
        xiaoshuo_mingzi_jianjieurl = re.findall(reg,response.text)
        self.logger.info(xiaoshuo_mingzi_jianjieurl)
        return xiaoshuo_mingzi_jianjieurl

    def parse_xiaoshuoming(self,response):
        total_page_num = self.get_total_page_num(response)
        base_url = response.url.split('_')[0]
        self.get_xiaoshuo_mingzi_jianjieurl(response)
        for page_num in range(2,total_page_num):
            next_page_url = base_url+'_'+str(page_num)+'.html'
            next_response = requests.get(next_page_url)
            next_response.encoding = 'gbk'
            self.get_xiaoshuo_mingzi_jianjieurl(next_response)
        #yield Request(next_page_url, callback=self.parse_xiaoshuoming)
        pass