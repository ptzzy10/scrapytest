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

    def get_total_page_num(self,response):#获取某类小说总页数
        total_page_reg = r'<em id="pagestats">1/(.*?)</em>'
        numstr = re.findall(total_page_reg,response.text)
        total_page_num = int(numstr[0])
        self.logger.info('response.url = %s,tatal_page_num = %d' % (response.url, total_page_num))
        return total_page_num

    #获取小说名字及简介地址
    def get_novel_name_breifurl(self,response):
        reg = r'<a target="_blank" title="(.*?)" href="(.*?)" class="clearfix stitle">'
        novel_name_breifurl = re.findall(reg,response.text)
        self.logger.info(novel_name_breifurl)
        for url in novel_name_breifurl:
            self.logger.info("开始爬取[ %s ]主要信息，地址为[ %s ]"%(url[0],url[1]))
            self.get_novel_main_info(url[1])
        return novel_name_breifurl

    #获取小说主要信息，如：作者、内容简介、小说状态、最近更新时间
    def get_novel_main_info(self,breifurl):
        response = self.get_req(breifurl)
        reg_breif = r'<div id="waa".*?>(.*?)</div>'
        breif = re.findall(reg_breif,response.text)
        self.get_novel_main_info(breif)
        reg_pic = r'<img.*?src="(.*?)".*?>'
        pic = re.findall(reg_pic, response.text)


        novel_book_detail = response.xpath("//div[@class=bookDetail]/dl/dd")
        status = novel_book_detail.xpath('/ul/li/')

        author = novel_book_detail[1].extract()

        #last_update_time = Column(DATE, nullable=False)  # 最后更新时间
       # breif = Column(String(1024), nullable=False)  # 简介
       # total_charpter_url = Column(String(100), nullable=False)  # 总章节地址

    def parse_xiaoshuoming(self,response):
        total_page_num = self.get_total_page_num(response)
        base_url = response.url.split('_')[0]
        self.get_novel_name_breifurl(response)
        for page_num in range(2,total_page_num):
            next_page_url = base_url+'_'+str(page_num)+'.html'
            next_response = requests.get(next_page_url)
            next_response.encoding = 'gbk'
            self.get_novel_name_breifurl(next_response)
        #yield Request(next_page_url, callback=self.parse_xiaoshuoming)
        pass

    def get_req(self,url):
        response = requests.get(url)
        response.encoding = 'gbk'
        return response

    def get_novel_main_info_of_onesort(self,sort_url):#获取某个分类所有小说的主要信息
        response = self.get_req(sort_url)
        #1.获取总的页数
        total_page_num = self.get_total_page_num(response)
        #2.获取第一页里面所有小说信息
        self.get_novel_name_breifurl(response)



    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        fenlei_urls = response.xpath("//ul[@class='channel-nav-list']/li/a/@href").extract()
        fenlei_ming = response.xpath("//ul[@class='channel-nav-list']/li/a/text()").extract()
        item = NovelSortItem()

        for i in range(len(fenlei_ming)):
            item['sort_name'] = fenlei_ming[i]
            item['sort_url'] = fenlei_urls[i]
            yield  item
        self.logger.info('========小说分类爬取完毕，共计%d分类'%(len(fenlei_ming)))

        #return
        for i in range(len(fenlei_ming)):
            sort_name = fenlei_ming[i]
            sort_url = fenlei_urls[i]
            self.logger.info('开始爬取 [%s] 小说'%(sort_name))
            self.get_novel_main_info_of_onesort(sort_url)


        for url in fenlei_urls:
            yield Request(url, callback=self.parse_xiaoshuoming)

