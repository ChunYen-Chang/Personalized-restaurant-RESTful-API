# import packages
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.types import *


# declare the basemodel
BaseModel = declarative_base()


# define the User, RestaurantInf, and Tweet class
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
 

class Tweet(BaseModel):
    __tablename__ = 'Tweet'
    tweet_id = Column(Integer, autoincrement=True, primary_key=True)
    tweet_user = Column(String(512))
    tweet_text = Column(String(512))
    tweet_text_time = Column(String(512))

 
# create user and Restaurant table in Mysql database    
engine = create_engine("mysql+mysqlconnector://id:pw@ec2-54-68-247-255.us-west-2.compute.amazonaws.com:3306/restaurant")
BaseModel.metadata.create_all(engine)
    
