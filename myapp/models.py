from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Fruit(Base):
    __tablename__ = "fruits"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255))


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    fruit_id = Column(Integer, ForeignKey("fruits.id"), nullable=False)
    quantity = Column(Integer, default=1)

    fruit = relationship("Fruit", backref="cart_items")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", backref="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    fruit_id = Column(Integer, ForeignKey("fruits.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float)

    fruit = relationship("Fruit")
