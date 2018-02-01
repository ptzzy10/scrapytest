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
from coolscrapy.models import db_connect, create_news_table, Article, XMLInfo, CSVInfo, NovelSort, NovelMainInfo


class CoolscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    print("session_scope 1")
    try:
        print("session_scope 2")
        yield session
        print("session_scope 3")
        session.commit()
    except:
        print("session_scope 4")
        session.rollback()
        raise
    finally:
        print("session_scope 5")
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

class NovelSortPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        print('=====NovelSortPipeline process_item')
        a = NovelSort(
                       sort_name=item["sort_name"],
                        sort_url=item["sort_url"],
                     )
        with session_scope(self.Session) as session:
            session.add(a)

class NovelMainInfoPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        print('=====NovelMainInfoPipeline process_item')
        a = NovelMainInfo(
            novel_name=item["novel_name"].encode("utf-8"),
            status=item["status"].encode("utf-8"),
            author=item["author"].encode("utf-8"),
            last_update_time=item["last_update_time"].encode("utf-8"),
            breif=item["breif"].encode("utf-8"),
            total_charpter_url=item["total_charpter_url"].encode("utf-8"),
            sort_id=item["sort_id"].encode("utf-8"),
        )
        with session_scope(self.Session) as session:
            session.add(a)

class NovelJuanPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        print('=====NovelJuanPipeline process_item')
        a = NovelMainInfo(
            juan_name=item["juan_name"].encode("utf-8"),
            novel_id=item["novel_id"].encode("utf-8"),
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
        print('=====NovelChapterPipeline process_item')
        a = NovelMainInfo(
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
        print('=====NovelContentPipeline process_item')
        a = NovelMainInfo(
            content=item["content"].encode("utf-8"),
            charpter_url=item["charpter_url"].encode("utf-8"),
            novel_id=item["novel_id"].encode("utf-8"),
            juan_id=item["juan_id"].encode("utf-8"),
            chapter_id=item["chapter_id"].encode("utf-8"),
        )
        with session_scope(self.Session) as session:
            session.add(a)

