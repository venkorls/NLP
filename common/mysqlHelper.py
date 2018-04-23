from sqlalchemy import Column, String, create_engine,BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Zs_extractInfo(Base):
    #表名
    __tablename__='zs_extractInfo'
    #表的结构
    id=Column(BIGINT,primary_key=True)
    topic=Column(String(1000))
    tags = Column(String(1000))
    keywords = Column(String(1000))
    comments = Column(String(1000))
    filename = Column(String(1000))
    filepath = Column(String(1000))

#初始化数据库连接
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/zsdsj')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

