from sqlalchemy import Column, Integer, String
from src.models.base import Base

class Customer(Base):
    __tablename__ = 'tb_customers'
    customer_id = Column(Integer, primary_key=True)
    customer_phone = Column(String)
