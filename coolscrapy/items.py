# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoolscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HuxiuItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    posttime = scrapy.Field()

class LinkItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    posttime = scrapy.Field()

class XMLItem(scrapy.Item):
    num = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    id = scrapy.Field()
    published = scrapy.Field()
    updated = scrapy.Field()
    content = scrapy.Field()

class CSVItem(scrapy.Item):
    id = scrapy.Field()
    username = scrapy.Field()
    password = scrapy.Field()
    birth = scrapy.Field()
    userid = scrapy.Field()
    status = scrapy.Field()
    ip = scrapy.Field()
    fname = scrapy.Field()
    lname = scrapy.Field()
    sex = scrapy.Field()
    city = scrapy.Field()
    friendnum = scrapy.Field()
    requestnum = scrapy.Field()
    lastlogintime = scrapy.Field()
    lastrequesttime = scrapy.Field()
    lasttagtime = scrapy.Field()
    advproduct = scrapy.Field()
    occupied = scrapy.Field()
    cookie = scrapy.Field()

class NovelSortItem(scrapy.Item):
    '''小说分类表'''
    sort_name = scrapy.Field()#分类名
    sort_url = scrapy.Field()#分类地址

class NovelMainInfoItem(scrapy.Item):
    '''小说主要信息'''
    novel_name = scrapy.Field()  # 小说名
    status =   scrapy.Field()  # 状态：连载中、完结
    author =  scrapy.Field()  # 作者名字
    last_update_time = scrapy.Field() #最后更新时间
    breif = scrapy.Field() #简介
    total_charpter_url = scrapy.Field()  # 总章节地址


class NovelJuanItem(scrapy.Item):
    '''小说卷本信息'''
    juan_name = scrapy.Field()  # 分卷名

class NovelChapterItem(scrapy.Item):
    '''小说章节信息'''
    chapter_name = scrapy.Field()  # 分类名
    charpter_url = scrapy.Field() # 章节内容地址

class NovelContentItem(scrapy.Item):
    '''小说内容信息'''
    content = scrapy.Field()  # 章节内容
