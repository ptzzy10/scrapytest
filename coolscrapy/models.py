#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc : 
"""
import datetime

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, DATE, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

from coolscrapy.settings import DATABASE


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

def create_seesion(engine):
    Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    session = Session_class()  # 生成session实例 #cursor
    return session


def _get_date():
    return datetime.datetime.now()

Base = declarative_base()


class Article(Base):
    """文章类"""
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    title = Column(String(100))
    body = Column(Text)
    publish_time = Column(String(30))
    source_site = Column(String(30))

class XMLInfo(Base):
    '''XML格式'''
    __tablename__ = 'xmlinfos'
    num = Column(Integer, primary_key=True)
    title =Column(String(100))
    link = Column(String(100))
    id = Column(String(100))
    published =  Column(String(30))
    updated =  Column(String(30))
    content =  Column(Text)

class CSVInfo(Base):
    '''CSV格式'''
    __tablename__ = 'csvinfos'

    id = Column(Integer, primary_key=True)
    username =  Column(String(30))
    password =  Column(String(30))
    birth =  Column(String(30))
    userid =  Column(String(30))
    status =  Column(String(30))
    ip =  Column(String(30))
    fname =  Column(String(30))
    lname =  Column(String(30))
    sex =  Column(String(30))
    city =  Column(String(30))
    friendnum = Column(Integer)
    requestnum = Column(Integer)
    lastlogintime =  Column(String(30))
    lastrequesttime =  Column(String(30))
    lasttagtime =  Column(String(30))
    advproduct =  Column(String(30))
    occupied =  Column(String(30))
    cookie =  Column(String(200))


class NovelSort(Base):
    '''小说分类表'''
    __tablename__ = 'novel_sort'

    sort_id = Column(Integer,primary_key=True)
    sort_name = Column(String(30),unique=True,nullable=False)#分类名
    sort_url = Column(String(100),nullable=False)#分类地址

class NovelMainInfo(Base):
    '''小说主要信息'''
    __tablename__ = 'novel_main_info'

    novel_id = Column(Integer, primary_key=True)
    novel_name = Column(String(50),unique=True,nullable=False)  # 小说名
    status =  Column(String(10),nullable=False)  # 状态：连载中、完结
    author = Column(String(30),nullable=False)  # 作者名字
    last_update_time = Column(DATE,nullable=False) #最后更新时间
    breif = Column(String(1024),nullable=False) #简介
    total_charpter_url = Column(String(100),nullable=False)  # 总章节地址
    sort_name = Column(String(30), nullable=False)  # 所属分类 ------外键关联------
#    sort_name = Column(String(30), ForeignKey("novel_sort.sort_id"))  # 所属分类 ------外键关联------
    # 这个nb，允许你在NovelMainInfo表里通过backref字段反向查出所有它在NovelSort表里的关联项数据
    #novel_sort = relationship("NovelSort", backref="my_sort")  # 添加关系，反查（在内存里）

class NovelJuan(Base):
    '''小说卷本信息'''
    __tablename__ = 'novel_juan'

    juan_id = Column(Integer, primary_key=True)
    juan_name = Column(String(100), unique=True,nullable=False)  # 分卷名
    novel_name = Column(String(50), nullable=False)  # 所属小说 ------外键关联------
#    novel_name = Column(String(50), ForeignKey("novel_main_info.novel_id"))  # 所属小说 ------外键关联------
    # 这个nb，允许你在NovelJuan表里通过backref字段反向查出所有它在NovelMainInfo表里的关联项数据
    #novel_main_info = relationship("NovelMainInfo", backref="my_novel")  # 添加关系，反查（在内存里）

class NovelChapter(Base):
    '''小说章节信息'''
    __tablename__ = 'novel_chapter'

    chapter_id = Column(Integer, primary_key=True)
    chapter_name = Column(String(100), unique=True,nullable=False)  # 分类名
    content_url = Column(String(100), nullable=False)  # 章节内容地址
    novel_name = Column(String(50), nullable=False)  # 所属小说 ------外键关联------
    juan_name = Column(String(100), nullable=False)  # 所属卷本 ------外键关联------
#    novel_name = Column(String(50), ForeignKey("novel_main_info.novel_id"))  # 所属小说 ------外键关联------
#    juan_name = Column(String(100), ForeignKey("novel_juan.juan_id"))  # 所属卷本 ------外键关联------

    # 这个nb，允许你在NovelMainInfo表里通过backref字段反向查出所有它在NovelSort表里的关联项数据
    #novel_main_info = relationship("NovelMainInfo", backref="my_novel")  # 添加关系，反查（在内存里）
    #novel_juan = relationship("NovelJuan", backref="my_juan")  # 添加关系，反查（在内存里）

class NovelContent(Base):
    '''小说内容信息'''
    __tablename__ = 'novel_content'

    content_id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)  # 章节内容
    novel_name = Column(String(50), nullable=False)  # 所属小说 ------外键关联------
    juan_name = Column(String(100), nullable=False)  # 所属卷本 ------外键关联------
    chapter_name = Column(String(100), nullable=False)  # 所属章节 ------外键关联------
#    novel_name = Column(String(50), ForeignKey("novel_main_info.novel_id"))  # 所属小说 ------外键关联------
#    juan_name = Column(String(100), ForeignKey("novel_juan.juan_id"))  # 所属卷本 ------外键关联------
 #   chapter_name = Column(String(100), ForeignKey("novel_chapter.chapter_id"))  # 所属章节 ------外键关联------
    # 这个nb，允许你在NovelMainInfo表里通过backref字段反向查出所有它在NovelSort表里的关联项数据
    #novel_main_info = relationship("NovelMainInfo", backref="my_novel")  # 添加关系，反查（在内存里）
    #novel_juan = relationship("NovelJuan", backref="my_juan")  # 添加关系，反查（在内存里）
    #novel_chapter = relationship("NovelChapter", backref="my_chapter")  # 添加关系，反查（在内存里）