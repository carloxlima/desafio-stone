from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.models.base import Base

class Order(Base):
    __tablename__ = 'tb_orders'
    order_id = Column(Integer, primary_key=True)
    order_number = Column(String)
    provider = Column(String)
    technician_email = Column(String)
    cancellation_reason_id = Column(Integer, ForeignKey("tb_cancellation_reasons.id"))
    arrival_date = Column(DateTime)
    deadline_date = Column(DateTime)
    last_modified_date = Column(DateTime)
