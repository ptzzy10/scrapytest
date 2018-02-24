# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from contextlib import contextmanager

import scrapy
import requests
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sqlalchemy.orm import sessionmaker

from coolscrapy.items import HuxiuItem, LinkItem, NovelSortItem, NovelMainInfoItem, NovelJuanItem, NovelChapterItem,NovelContentItem
import re
#链接爬取蜘蛛，专门为那些爬取有特定规律的链接内容而准备的。
from coolscrapy.models import NovelMainInfo, db_connect, create_news_table, NovelChapter, NovelContent


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class QuanshuSpider(scrapy.Spider):
    name = "quanshu"
    allowed_domains = ["quanshuwang.com"]
    start_urls = ["http://www.quanshuwang.com/index.html"]

    novel_main_info_priority = 300
    novel_total_charpter_info_priority = 200
    novel_one_charpter_content_priority = 100

    geted_all_novel_names = ''

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        with session_scope(self.Session) as session:
            # 查询该分类是否已存在
            self.geted_all_novel_names = session.query(NovelMainInfo, NovelMainInfo.novel_name).all()

        pass


    #获取小说内容
    def parse_novel_one_charpter_content(self,response):
        #response = self.get_req(content_url)
        hxs = Selector(text=response.text)
        content_div = hxs.xpath('//div[@id="content"]')
        content = hxs.xpath('//div[@id="content"]')[0].extract()
        #self.logger.info(content)
        self.logger.info("获取到小说章节内容。")
        novel_content_item = NovelContentItem()
        novel_content_item['novel_name'] = response.meta['novel_name']
        novel_content_item['juan_name'] = response.meta['juan_name']
        novel_content_item['chapter_name'] = response.meta['chapter_name']
        novel_content_item['content'] = content

        yield novel_content_item
        pass

    #获取小说总卷及章节目录
    def parse_novel_total_charpter_info(self,response):
        #response = self.get_req(charpter_url)
        hxs = Selector(text=response.text)
        juan_names = hxs.xpath('//div[@class="dirtitone"]/h2/text()').extract()
        total_juan_num = len(juan_names)
        novel_name = response.meta['novel_name']

        juan_item = NovelJuanItem()
        juan_item['juan_name'] = juan_names
        juan_item['novel_name'] = novel_name
        yield juan_item

        #chapterNum_div =  hxs.xpath('//div[@class="chapterNum"]')[0]
        #next_dir = chapterNum_div.xpath('./ul/div[@class="dirtitone"]')[0]
        next_dir = hxs.xpath('//div[@class="dirtitone"]')[0]

        chapterItem = NovelChapterItem()
        for i in range(total_juan_num):
            chapterItem['juan_name'] = next_dir.xpath('h2/text()').extract()[0]
            chapterItem['chapter_name'] = next_dir.xpath('../div/li/a/text()').extract()
            chapterItem['content_url'] = next_dir.xpath('../div/li/a/@href').extract()
            chapterItem['novel_name'] = novel_name
            next_dirs = next_dir.xpath('../div/div[@class="dirtitone"]')
            if(next_dirs):
                next_dir = next_dirs[0]

            yield chapterItem
            #if i==10:
            #    break
            '''
            self.logger.info("开始爬取小说章节内容。")
            for j in range(len(chapterItem['content_url'])):
                self.logger.info('章节名字:[%s] 章节地址:[%s]' % (chapterItem['chapter_name'][j], chapterItem['content_url'][j]))
                # self.get_novel_one_charpter_content(content_urls[j])
                yield Request(chapterItem['content_url'][j], callback=self.parse_novel_one_charpter_content,meta={'novel_name':novel_name,'juan_name':chapterItem['juan_name'] ,'chapter_name':chapterItem['chapter_name'][j]},priority=self.novel_one_charpter_content_priority,dont_filter=True)
                #if j == 10:
                #   break
        '''
            self.logger.info("暂不爬取小说章节内容。")
       #pass

    #获取小说主要信息，如：作者、内容简介、小说状态、最近更新时间
    def parse_novel_main_info(self,response):
        #response = self.get_req(breifurl)
        hxs = Selector(text=response.text)
        breif_div = hxs.xpath('//div[@id="waa"]//text()')
        breif = breif_div[0].extract()
        total_charpter_url_a = hxs.xpath('//a[@class="reader"]/@href')
        total_charpter_url = total_charpter_url_a[0].extract()
        book_detail_div = hxs.xpath('//div[@class="bookDetail"]')[0]
        status = book_detail_div.xpath('dl/dd/text()')[0].extract()
        author = book_detail_div.xpath('dl/dd/text()')[1].extract()
        last_update_time_lis = book_detail_div.xpath('dl/dd/ul/li/text()')
        if last_update_time_lis:
            last_update_time = last_update_time_lis[0].extract()[2:-1]
        novel_name = response.meta['novel_name']
        sort_name = response.meta['sort_name']
        self.logger.info("小说:[%s] 简介:[%s] 总章节地址:[%s] 小说状态:[%s] 作者:[%s] 最后更新时间:[%s]" % (novel_name,breif,total_charpter_url,status,author,last_update_time))
        item = NovelMainInfoItem()
        item['novel_name'] = novel_name
        item['sort_name'] = sort_name
        item['status'] = status
        item['author'] = author
        item['last_update_time'] = last_update_time
        item['breif'] = breif
        item['total_charpter_url'] = total_charpter_url
        yield item

        #self.get_novel_total_charpter_info(total_charpter_url)
        #total_charpter_url = 'http://www.quanshuwang.com/book/2/2703'
        yield Request(total_charpter_url, callback=self.parse_novel_total_charpter_info,meta={'novel_name':novel_name},priority=self.novel_total_charpter_info_priority,dont_filter=True)
        pass

        #获取某个分类小说所有小说的简介地址
    '''def get_onesort_total_novel_breifurl(self,sort_url,total_pagenum):

        base_url = sort_url.split('_')[0]


        for i in range(1,total_pagenum):
            url = base_url+i+'.html'
            Request(url[1], callback=self.parse_novel_main_info, meta={'novel_name': url[0], 'sort_name': sort_name},
                    dont_filter=True)

        return novel_name_breifurl

    '''
    # 获取某个分类所有小说的主要信息
    def parse_novel_main_info_of_onesort(self,response):
        sort_name = response.meta['sort_name']
        self.logger.info('小说分类:[%s] ,response.url:[%s]' % (sort_name,response.url))
        reg = r'<a target="_blank" title="(.*?)" href="(.*?)" class="clearfix stitle">'
        novel_name_breifurl = re.findall(reg, response.text)
        self.logger.info(novel_name_breifurl)

        for url in novel_name_breifurl:
            find_tag = False
            novel_name = url[0]
            novel_main_info_url = url[1]
            self.logger.info("开始爬取[ %s ]主要信息，地址为[ %s ]" % (novel_name, novel_main_info_url))
            for novel_row in self.geted_all_novel_names:
                #self.logger.info("novel_row.novel_name=[%s]"%(novel_row.novel_name))
                if novel_name == novel_row.novel_name:
                    self.logger.info("该小说已存在[%s]" % (novel_row.novel_name))
                    find_tag = True
                    break


            if find_tag==False:
                self.logger.info("增加新小说[%s]" % (novel_name))
                yield Request(novel_main_info_url, callback=self.parse_novel_main_info,meta={'novel_name':novel_name,'sort_name':sort_name},priority=self.novel_main_info_priority,dont_filter=True)

    pass


    # 获取某个分类所有小说的主要信息
    def parse_all_novel_of_onesort(self,response):
        sort_name = response.meta['sort_name']
        total_page_reg = r'<em id="pagestats">1/(.*?)</em>'
        numstr = re.findall(total_page_reg, response.text)
        total_page_num = int(numstr[0])
        self.logger.info('小说分类:[%s] ,response.url:[%s] ,小说分类总页数:[%d]' % (sort_name,response.url, total_page_num))
        base_url = (response.url.split('_'))[0]

        for page_num in range(1,total_page_num):
            url = base_url+"_"+str(page_num)+".html"
            yield Request(url, callback=self.parse_novel_main_info_of_onesort,meta={'sort_name':sort_name},priority=self.novel_main_info_priority, dont_filter=True)

        pass

    #查询NovelChapter表中哪些文章已获取并置标志位
    def zhenglishuju(self):
        self.logger.info("开始整理数据库")
        with session_scope(self.Session) as session:
            #查询该分类是否已存在
            all_chapters = session.query(NovelChapter,NovelChapter.chapter_name).all()
            all_contents = session.query(NovelContent,NovelContent.chapter_name).all()
            for chap_row in all_chapters:
                self.logger.info("chap_row.chapter_name=[%s]"%(chap_row.chapter_name))
                find_tag = False
                for cont_row in all_contents:
                    #self.logger.info("cont_row.chapter_name=[%s]" % (cont_row.chapter_name))
                    if chap_row.chapter_name == cont_row.chapter_name:
                        find_tag = True
                        break

                if find_tag:
                    self.logger.info("该章节已存储[ %s ]" % (chap_row.chapter_name))
                    chap_row.NovelChapter.get_content_tag = 1
                    session.commit()
                else:
                    self.logger.info("未存储[ %s ]" % (chap_row.chapter_name))

    # 获取小说内容
    def parse_novel_one_charpter_content_by_NovelChapter(self, response):
        # response = self.get_req(content_url)
        hxs = Selector(text=response.text)
        content_div = hxs.xpath('//div[@id="content"]')
        content = hxs.xpath('//div[@id="content"]')[0].extract()
        # self.logger.info(content)
        self.logger.info("parse_novel_one_charpter_content_by_NovelChapter 获取到小说章节内容。")
        novel_content_item = NovelContentItem()
        novel_content_item['novel_name'] = response.meta['novel_name']
        novel_content_item['juan_name'] = response.meta['juan_name']
        novel_content_item['chapter_name'] = response.meta['chapter_name']
        novel_content_item['content'] = content

        yield novel_content_item
        session = response.meta['session']
        chap_row = response.meta['chap_row']
        chap_row.NovelChapter.get_content_tag = 1
        session.commit()
        #pass

    #根据NovelChapter get_content_tag标志位，如果未获取则获取内容，并置标志位
    def get_content_by_NovelChapter(self):
        self.logger.info("开始根据数据库获取文章内容")
        with session_scope(self.Session) as session:
            #查询该分类是否已存在
            all_chapters = session.query(NovelChapter,NovelChapter.chapter_name).all()
           # all_contents = session.query(NovelContent,NovelContent.chapter_name).all()
            for chap_row in all_chapters:
                if chap_row.NovelChapter.get_content_tag == b'\x01':
                    self.logger.info("该文章已获取 [ %s ]"%(chap_row.NovelChapter.chapter_name))
                    continue
                else:
                    url = chap_row.NovelChapter.content_url
                    novel_name = chap_row.NovelChapter.novel_name
                    juan_name = chap_row.NovelChapter.juan_name
                    chapter_name = chap_row.NovelChapter.chapter_name
                    self.logger.info("新文章 [ %s ]" % (chap_row.NovelChapter.chapter_name))
                    yield Request(url,
                                  callback=self.parse_novel_one_charpter_content_by_NovelChapter,
                                  meta={'novel_name': novel_name, 'juan_name': juan_name,'chapter_name': chapter_name,'session':session,'chap_row':chap_row},
                                  priority=self.novel_one_charpter_content_priority,dont_filter=True)
        pass

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        #self.zhenglishuju()
        #self.get_content_by_NovelChapter()


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
            self.logger.info('开始爬取 [%s] 分类小说'%(sort_name))
            if sort_name == '玄幻魔法':
                priority = self.novel_main_info_priority + 12
            elif sort_name == '武侠修真':
                priority = self.novel_main_info_priority + 11
            elif sort_name == '纯爱耽美':
                priority = self.novel_main_info_priority + 10
            elif sort_name == '都市言情':
                priority = self.novel_main_info_priority + 9
            elif sort_name == '职场校园':
                priority = self.novel_main_info_priority + 8
            elif sort_name == '穿越重生':
                priority = self.novel_main_info_priority + 7
            elif sort_name == '历史军事':
                priority = self.novel_main_info_priority + 6
            elif sort_name == '网游动漫':
                priority = self.novel_main_info_priority + 5
            elif sort_name == '恐怖灵异':
                priority = self.novel_main_info_priority + 4
            elif sort_name == '科幻小说':
                priority = self.novel_main_info_priority + 3
            elif sort_name == '美文名著':
                priority = self.novel_main_info_priority + 2
            elif sort_name == '热门推荐':
                priority = self.novel_main_info_priority + 1

            yield Request(sort_url, callback=self.parse_all_novel_of_onesort,meta={'sort_name':sort_name},priority=priority, dont_filter=True)
            #if i==10:
            #    break

