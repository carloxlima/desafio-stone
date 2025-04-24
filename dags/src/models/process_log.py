from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Boolean, func
from src.models.base import Base


class ProcessLog(Base):
    __tablename__ = "tb_process_log"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), unique=True, nullable=False)
    process_status = Column(String(50), nullable=False)
    process_time = Column(TIMESTAMP, server_default=func.now())
    error_message = Column(Text)
    processed = Column(Boolean, default=False)
    step = Column(Integer, nullable=False)
