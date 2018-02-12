# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import redis
import json
import logging
from contextlib import contextmanager

from scrapy import signals
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from coolscrapy.models import db_connect, create_news_table, Article, XMLInfo, CSVInfo, NovelSort, NovelMainInfo, \
    NovelJuan, NovelChapter


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
        print("session_scope commit")
        session.commit()
    except:
        print("session_scope rollback")
        session.rollback()
        raise
    finally:
        print("session_scope close")
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
            stored_novel_sort = session.query(NovelSort).filter(NovelSort.sort_name == item["sort_name"]).first()
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
            status=cur_process_item["status"],
            author=cur_process_item["author"],
            last_update_time=cur_process_item["last_update_time"],
            breif=cur_process_item["breif"],
            total_charpter_url=cur_process_item["total_charpter_url"],
        )
        with session_scope(self.Session) as session:
            stored_novel_sort = session.query(NovelMainInfo).filter(NovelMainInfo.novel_name == cur_process_item["novel_name"]).first()
            # 在stu2表，查到StudyRecord表的记录
            if (stored_novel_sort):
                print("该小说已经存储，sort_name=%s" % (cur_process_item["novel_name"]))
            else:
                print("增加新小说，sort_name=%s" % (cur_process_item["novel_name"]))
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
        for name in juan_names:
            a = NovelJuan(
                juan_name=name,
                #novel_id=item["novel_id"].encode("utf-8"),
            )
            with session_scope(self.Session) as session:
                session.add(a)

class NovelChapterPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        print('=====小说章节名存储 process_item')
        a = NovelChapter(
            chapter_name=item["chapter_name"].encode("utf-8"),
            charpter_url=item["charpter_url"].encode("utf-8"),
            novel_id=item["novel_id"].encode("utf-8"),
            juan_id=item["juan_id"].encode("utf-8"),
        )
        with session_scope(self.Session) as session:
            session.add(a)


class NovelContentPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        print('=====小说内容存储 process_item')
        a = NovelMainInfo(
            content=item["content"].encode("utf-8"),
            charpter_url=item["charpter_url"].encode("utf-8"),
            novel_id=item["novel_id"].encode("utf-8"),
            juan_id=item["juan_id"].encode("utf-8"),
            chapter_id=item["chapter_id"].encode("utf-8"),
        )
        with session_scope(self.Session) as session:
            session.add(a)

