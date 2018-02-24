# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import redis
import json
import logging
import time
from contextlib import contextmanager

from scrapy import signals
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from coolscrapy.models import db_connect, create_news_table, Article, XMLInfo, CSVInfo, NovelSort, NovelMainInfo, \
    NovelJuan, NovelChapter, NovelContent


class CoolscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

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

class ArticleDataBasePipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        print('============ArticleDataBasePipeline process_item')
        '''a = Article(url=item["url"],
                    title=item["title"].encode("utf-8"),
                    publish_time=item["publish_time"].encode("utf-8"),
                    body=item["body"].encode("utf-8"),
                    source_site=item["source_site"].encode("utf-8"))
                   '''
        a = Article(url=item["link"],
                    title=item["title"].encode("utf-8"),
                    publish_time=item["posttime"].encode("utf-8"),
                    )
        with session_scope(self.Session) as session:
            print("session.add ")
            session.add(a)

    def close_spider(self, spider):
        pass

global num2
num2 = 0

class XMLDataPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        print("This method is called when the spider is opened.")
        pass

    def process_item(self, item, spider):
        global num2
        num2 += 1
        print('=====XMLDataPipeline process_item num=',num2)
        a = XMLInfo( num = num2,
                    title=item["title"].encode("utf-8"),
                    link=item["link"].encode("utf-8"),
                    id=item["id"].encode("utf-8"),
                    published=item["published"].encode("utf-8"),
                    updated=item["updated"].encode("utf-8"),
                     content = item["content"].encode("utf-8"),
                    )
        with session_scope(self.Session) as session:
            print("session.add ")
            session.add(a)

    def close_spider(self, spider):
        print("=====close_spider")
        pass

class CSVDataPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        print("This method is called when the spider is opened.")
        pass

    def process_item(self, item, spider):

        print('=====CSVDataPipeline process_item num=')
        if(item['id'] == 'id'):
            print('这是第一行')
            return
        a = CSVInfo( id = int(item["id"]),
                     username=item["username"].encode("utf-8"),
                     password=item["password"].encode("utf-8"),
                     birth= item["birth"].encode("utf-8"),
                     userid= item["userid"].encode("utf-8"),
                     status= item["status"].encode("utf-8"),
                     ip= item["ip"].encode("utf-8"),
                     fname= item["fname"].encode("utf-8"),
                     lname= item["lname"].encode("utf-8"),
                     sex= item["sex"].encode("utf-8"),
                     city= item["city"].encode("utf-8"),
                     friendnum= int(item["friendnum"]),
                     requestnum= int(item["requestnum"]),
                     lastlogintime= item["lastlogintime"].encode("utf-8"),
                     lastrequesttime= item["lastrequesttime"].encode("utf-8"),
                     lasttagtime= item["lasttagtime"].encode("utf-8"),
                     advproduct= item["advproduct"].encode("utf-8"),
                     occupied= item["occupied"].encode("utf-8"),
                     cookie= item["cookie"].encode("utf-8"),
                    )
        with session_scope(self.Session) as session:
            print("session.add ")
            session.add(a)

    def close_spider(self, spider):
        print("=====close_spider")
        pass

cur_pipeline_name = ''
cur_process_item =''

class NovelSortPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        global cur_pipeline_name,cur_process_item
        cur_pipeline_name = item.__class__.__name__
        cur_process_item = item
        print("NovelSortPipeline cur_pipeline_name:[%s]"%cur_pipeline_name)
        if(cur_pipeline_name != 'NovelSortItem'):
            return
        print('=====小说分类存储 process_item ')

        sort_name_tmp = item["sort_name"]
        sort_url_tmp = item["sort_url"]
        a = NovelSort(
                       sort_name=sort_name_tmp,
                        sort_url=sort_url_tmp,
                     )

        with session_scope(self.Session) as session:
            t0 = time.clock()
            stored_novel_sort = session.query(NovelSort).filter(NovelSort.sort_name == item["sort_name"]).first()
            t1 = time.clock()
            print("分类查询耗时: ", t1 - t0)
            # 在stu2表，查到StudyRecord表的记录
            if(stored_novel_sort):
                print("该分类已经存储，sort_name=%s"%(sort_name_tmp))
            else:
                print("增加新分类，sort_name=%s" % (sort_name_tmp))
                session.add(a)

class NovelMainInfoPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        global cur_pipeline_name,cur_process_item
        print("NovelMainInfoPipeline cur_pipeline_name:[%s]" % cur_pipeline_name)
        if (cur_pipeline_name != 'NovelMainInfoItem'):
            return

        print('=====小说主要信息存储 process_item')
        a = NovelMainInfo(
            novel_name=cur_process_item["novel_name"],
            sort_name=cur_process_item["sort_name"],
            status=cur_process_item["status"],
            author=cur_process_item["author"],
            last_update_time=cur_process_item["last_update_time"],
            breif=cur_process_item["breif"],
            total_charpter_url=cur_process_item["total_charpter_url"],
        )
        with session_scope(self.Session) as session:
            #查询该分类是否已存在
            t0 = time.clock()
            stored_novel_sort = session.query(NovelMainInfo).filter(NovelMainInfo.novel_name == cur_process_item["novel_name"]).first()
            t1 = time.clock()
            print("小说查询耗时: ", t1 - t0)
            # 在stu2表，查到StudyRecord表的记录
            if (stored_novel_sort):
                print("该小说已经存储，sort_name=%s" % (cur_process_item["novel_name"]))
            else:
                print("增加新小说，novel_name=%s" % (cur_process_item["novel_name"]))
                session.add(a)


class NovelJuanPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        global cur_pipeline_name, cur_process_item
        print("NovelJuanPipeline cur_pipeline_name:[%s]" % cur_pipeline_name)
        if (cur_pipeline_name != 'NovelJuanItem'):
            return

        print('=====小说卷名存储 process_item')
        juan_names = cur_process_item['juan_name']
        novel_name2 = cur_process_item['novel_name']
        for name in juan_names:
            a = NovelJuan(
                juan_name=name,
                novel_name=novel_name2,
            )
            with session_scope(self.Session) as session:
                # 查询是否已存在
                t0 = time.clock()
                stored_tag = session.query(NovelJuan).filter(NovelJuan.juan_name == name).first()
                t1 = time.clock()
                print("卷名查询耗时: ", t1 - t0)
                if (stored_tag):
                    print("该卷名已经存储，juan_name=%s" % (name))
                else:
                    print("增加新卷名，juan_name=%s" % (name))
                    session.add(a)

class NovelChapterPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        global cur_pipeline_name, cur_process_item
        print("NovelChapterPipeline cur_pipeline_name:[%s]" % cur_pipeline_name)
        if (cur_pipeline_name != 'NovelChapterItem'):
            return

        print('=====小说章节名存储 process_item')

        juan_name2 = cur_process_item['juan_name']
        chapter_names = cur_process_item['chapter_name']
        content_urls = cur_process_item['content_url']
        novel_name2 = cur_process_item['novel_name']

        for i in range(len(chapter_names)):
            a = NovelChapter(
                chapter_name=chapter_names[i],
                content_url=content_urls[i],
                novel_name = novel_name2,
                juan_name = juan_name2,
                get_content_tag = 0,
            )
            with session_scope(self.Session) as session:
                # 查询是否已存在
               # t0 = time.clock()
                stored_tag = session.query(NovelChapter).filter(NovelChapter.chapter_name == chapter_names[i]).first()
                #t1 = time.clock()
              #  print("章节查询耗时: ", t1 - t0)
                if (stored_tag):
                    print("该章节已经存储，chapter_names=%s" % (chapter_names[i]))
                else:
                    print("增加新章节，chapter_names=%s" % (chapter_names[i]))
                    session.add(a)


class NovelContentPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        global cur_pipeline_name, cur_process_item
        print("NovelContentPipeline cur_pipeline_name:[%s]" % cur_pipeline_name)
        if (cur_pipeline_name != 'NovelContentItem'):
            return

        print('=====小说内容存储 process_item')

        novel_name2 = cur_process_item['novel_name']
        juan_name2 = cur_process_item['juan_name']
        chapter_name2 = cur_process_item['chapter_name']
        content2 = cur_process_item['content']

        a = NovelContent(
            content=content2,
            novel_name=novel_name2,
            juan_name=juan_name2,
            chapter_name=chapter_name2,
        )
        with session_scope(self.Session) as session:                # 查询是否已存在
            t0 = time.clock()
            #stored_tag = session.query(NovelContent).filter(NovelContent.chapter_name == chapter_name2).first()
            stored_tag = 0
            t1 = time.clock()
            print("内容查询耗时: ",t1 - t0)
            if (stored_tag):
                print("该章节内容已经存储，chapter_names=%s" % (chapter_name2))
            else:
                print("增加新章节内容，chapter_names=%s" % (chapter_name2))
                session.add(a)

