
'''
参考文章链接：
http://blog.csdn.net/fgf00/article/details/52949973
'''
from sqlalchemy import create_engine, DATE, ForeignKey
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relationship

#第一种方式创建数据库
#engine = create_engine("mysql+pymysql://root:123456@localhost/test",
#                                    encoding='utf-8', echo=True)
engine = create_engine("mysql+pymysql://root:123456@localhost:3307/test?charset=utf8")

Base = declarative_base()

class User(Base):
    __tablename__ = 'user7'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

Base.metadata.create_all(engine)  # 创建表结构 （这里是父类调子类）
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
Session = Session_class()  # 生成session实例，相当于游标

#插入一条数据
sqlid = 54
user_obj = User(id=sqlid,name="你好",password="123456")  # 生成你要创建的数据对象
#print(user_obj.name,user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None

Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
print(user_obj.name,user_obj.id) #此时也依然还没创建
Session.commit() #现此才统一提交，创建数据

# 查询
print('查询')
my_user = Session.query(User).filter_by(id=sqlid).first()  # 查询
print(my_user.id,my_user.name,my_user.password)
#my_users = Session.query(User).filter_by().all()  # 查询所有
#print(my_users[0].id,my_users[0].name,my_users[0].password)
#print(my_user)
'''
#多条件查询
#filter_by与filter
print('多条件查询 filter_by与filter')
my_user1 = Session.query(User).filter(User.id>2).all()
my_user2 = Session.query(User).filter_by(id=27).all()  # filter_by相等用‘=’
my_user3 = Session.query(User).filter(User.id==27).all()  # filter相等用‘==’
print(my_user1,'\n',my_user2,'\n',my_user3)
objs = Session.query(User).filter(User.id>0).filter(User.id<7).all()
print(objs)

#修改
print('修改')
my_user = Session.query(User).filter_by(name="fgf").first()
my_user.name = "fenggf"  # 查询出来之后直接赋值修改
my_user.password = "123qwe"
Session.commit()
'''

class Stu2(Base):
    __tablename__ = "stu2"
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    register_date = Column(DATE,nullable=False)
    def __repr__(self):
        return "<%s name:%s>" % (self.id, self.name)

class StudyRecord(Base):
    __tablename__ = "study_record"
    id = Column(Integer, primary_key=True)
    day = Column(Integer,nullable=False)
    status = Column(String(32),nullable=False)
    stu_id = Column(Integer,ForeignKey("stu2.id"))  #------外键关联------
    #这个nb，允许你在user表里通过backref字段反向查出所有它在stu2表里的关联项数据
    stu2 = relationship("Stu2", backref="my_study_record")  # 添加关系，反查（在内存里）
    def __repr__(self):
        return "<%s day:%s status:%s>" % (self.stu2.name, self.day,self.status)

Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

s1 = Stu2(name="A",register_date="2014-05-21")
s2 = Stu2(name="J",register_date="2014-03-21")
s3 = Stu2(name="R",register_date="2014-02-21")
s4 = Stu2(name="E",register_date="2013-01-21")

study_obj1 = StudyRecord(day=1,status="YES", stu_id=1)
study_obj2 = StudyRecord(day=2,status="NO", stu_id=1)
study_obj3 = StudyRecord(day=3,status="YES", stu_id=1)
study_obj4 = StudyRecord(day=1,status="YES", stu_id=2)

session.add_all([s1,s2,s3,s4,study_obj1,study_obj2,study_obj3,study_obj4])  # 创建
session.commit()

stu_obj = session.query(Stu2).filter(Stu2.name=="a").first()  # 查询
# 在stu2表，查到StudyRecord表的记录
print(stu_obj.my_study_record)  # 查询A一共上了几节课