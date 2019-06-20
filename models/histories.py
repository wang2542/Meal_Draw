from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import uuid
import datetime


class Histories(Base):
    __tablename__ = 'histories'
    id = Column(String(50), primary_key=True)
    created_time = Column(DateTime(), nullable=False)
    restaurant_id = Column(String(50), ForeignKey('restaurants.id'))
    # Column(类型（最大长度），数据类型)

    def __init__(self, restaurant_id):
        self.id = str(uuid.uuid4())
        self.created_time = datetime.datetime.now()
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<Histories %r>' % (self.name)