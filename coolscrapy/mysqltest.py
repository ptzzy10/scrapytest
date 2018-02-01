import pymysql
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:123456@localhost:3307/test?charset=utf8",echo=True,encoding='utf-8',convert_unicode=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'tb_user3'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False, unique=True, comment=u"姓名")
    __table_args__ = {
    "mysql_charset": "utf8"
    }

Base.metadata.create_all(engine)  # 创建表结构 （这里是父类调子类）
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
Session = Session_class()  # 生成session实例，相当于游标
user_obj = User(id=1,name="张三")  # 生成你要创建的数据对象
#print(user_obj.name,user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None

Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
print(user_obj.name,user_obj.id) #此时也依然还没创建
Session.commit() #现此才统一提交，创建数据
'''
conn = pymysql.connect(
    host="127.0.0.1",
    port=3307,
    user='root',
    password='123456',
    db='test',
    charset='utf8'
)

cussor = conn.cursor()
cussor.execute("insert into test1(name) values(%s)", ("你好"))
# 提交，不然无法保存新建或者修改的数据
conn.commit()

# 关闭游标
cussor.close()
# 关闭连接
conn.close()
'''