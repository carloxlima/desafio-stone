from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base


class Customer(Base):
    __tablename__ = "tb_customers"
    __table_args__ = {"schema": "public"}

    customer_id = Column(Integer, primary_key=True)
    customer_code = Column(String)
    customer_phone = Column(String)

    addresses = relationship("Address", back_populates="customer")
    order = relationship("Order", back_populates="customer")


class Address(Base):
    __tablename__ = "tb_addresses"
    __table_args__ = {"schema": "public"}

    address_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(
        "public.tb_customers.customer_id"))
    city = Column(String)
    country = Column(String)
    country_state = Column(String)
    zip_code = Column(String)
    street_name = Column(String)
    neighborhood = Column(String)
    complement = Column(String)

    customer = relationship("Customer", back_populates="addresses")


class CancellationReason(Base):
    __tablename__ = "tb_cancellation_reasons"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    reason = Column(String, unique=True)

    order = relationship("Order", back_populates="cancellationreason")


class Order(Base):
    __tablename__ = "tb_orders"
    __table_args__ = {"schema": "public"}

    order_id = Column(Integer, primary_key=True)
    order_number = Column(String)
    provider = Column(String)
    technician_email = Column(String)
    cancellation_reason_id = Column(
        Integer, ForeignKey("public.tb_cancellation_reasons.id")
    )
    customer_id = Column(Integer, ForeignKey(
        "public.tb_customers.customer_id"))
    arrival_date = Column(DateTime)
    deadline_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    terminal_serial_number = Column(String(255), nullable=True)
    terminal_model = Column(String(100), nullable=True)
    terminal_type = Column(String(50), nullable=True)
    file_name = Column(String(255), nullable=False)

    customer = relationship("Customer", back_populates="order")
    cancellationreason = relationship(
        "CancellationReason", back_populates="order")
