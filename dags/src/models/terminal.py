from sqlalchemy import Column, Integer, String
from airflow.models.base import Base

class Terminal(Base):
    __tablename__ = 'tb_terminals'
    __table_args__ = {'schema': 'public'}

    terminal_id = Column(Integer, primary_key=True, autoincrement=True)
    terminal_serial_number = Column(String(255), unique=True, nullable=True)
    terminal_model = Column(String(100), nullable=True)
    terminal_type = Column(String(50), nullable=True)

    def __repr__(self):
        return (
            f"<Terminal(id={self.terminal_id}, "
            f"serial='{self.terminal_serial_number}', "
            f"model='{self.terminal_model}', "
            f"type='{self.terminal_type}')>"
        )
