from sqlalchemy import Column, Integer, String, ForeignKey
from src.models.base import Base

class Address(Base):
    __tablename__ = 'tb_addresses'
    address_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("tb_customers.customer_id"))
    city = Column(String)
    country = Column(String)
    country_state = Column(String)
    zip_code = Column(String)
    street_name = Column(String)
    neighborhood = Column(String)
    complement = Column(String)
