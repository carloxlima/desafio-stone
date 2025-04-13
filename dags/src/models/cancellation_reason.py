from sqlalchemy import Column, Integer, String
from src.models.base import Base

class CancellationReason(Base):
    __tablename__ = 'tb_cancellation_reasons'
    id = Column(Integer, primary_key=True)
    reason = Column(String, unique=True)
