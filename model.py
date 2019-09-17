from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.types import *


BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(512))    
    password = Column(String(20))


class RestaurantInf(BaseModel):
    __tablename__ = 'RestaurantInf'
    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512))
    address = Column(String(512))
    photo = Column(String(512))
    
    
engine = create_engine("mysql+mysqlconnector://id:pw@ec2-54-68-247-255.us-west-2.compute.amazonaws.com:3306/restaurant")

BaseModel.metadata.create_all(engine)
    
