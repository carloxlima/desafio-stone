from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base


class DimCustomer(Base):
    __tablename__ = 'dim_customers'

    customer_id = Column(Integer, primary_key=True)
    customer_phone = Column(String(20))
    addresses = relationship("DimAddress", back_populates="customer")
    orders = relationship("FctOrder", back_populates="customer")

# Dimensão: Endereços
class DimAddress(Base):
    __tablename__ = 'dim_addresses'

    address_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('dim_customers.customer_id'))
    city = Column(String(100))
    country = Column(String(100))
    country_state = Column(String(100))
    zip_code = Column(String(20))
    street_name = Column(String(255))
    neighborhood = Column(String(255))
    complement = Column(String(255))

    customer = relationship("DimCustomer", back_populates="addresses")

# Dimensão: Técnicos
class DimTechnician(Base):
    __tablename__ = 'dim_technicians'

    technician_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    orders = relationship("FctOrder", back_populates="technician")

# Dimensão: Terminais
class DimTerminal(Base):
    __tablename__ = 'dim_terminals'

    terminal_id = Column(Integer, primary_key=True)
    serial_number = Column(String(255), unique=True)
    model = Column(String(100))
    type = Column(String(50))
    orders = relationship("FctOrder", back_populates="terminal")

# Dimensão: Motivos de Cancelamento
class DimCancellationReason(Base):
    __tablename__ = 'dim_cancellation_reasons'

    id = Column(Integer, primary_key=True)
    reason = Column(String(255))
    orders = relationship("FctOrder", back_populates="cancellation_reason")

# Tabela Fato: Pedidos
class FctOrder(Base):
    __tablename__ = 'fct_orders'

    order_id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('dim_customers.customer_id'))
    address_id = Column(Integer, ForeignKey('dim_addresses.address_id'))
    terminal_id = Column(Integer, ForeignKey('dim_terminals.terminal_id'))
    technician_id = Column(Integer, ForeignKey('dim_technicians.technician_id'))
    cancellation_reason_id = Column(Integer, ForeignKey('dim_cancellation_reasons.id'))
    provider = Column(String(255))
    arrival_date = Column(DateTime)
    deadline_date = Column(DateTime)
    last_modified_date = Column(DateTime)

    customer = relationship("DimCustomer", back_populates="orders")
    technician = relationship("DimTechnician", back_populates="orders")
    terminal = relationship("DimTerminal", back_populates="orders")
    cancellation_reason = relationship("DimCancellationReason", back_populates="orders")
