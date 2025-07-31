from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean, DateTime, Date,
    ForeignKey, Table, func
)
from sqlalchemy.orm import declarative_base, relationship, backref
from datetime import datetime
Base = declarative_base()

# product_tags table also needs to be pure SQLAlchemy
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image = Column(String(200))
    weight = Column(Integer)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    expiration_date = Column(DateTime, nullable=True)
    date_added = Column(DateTime, default=func.now(), onupdate=func.now())
    dynamic_pricing_enabled = Column(Boolean, default=False)
    pending_price = Column(Float, nullable=True)
    target_daily_sales = Column(Float, nullable=True)
    sold_today = Column(Integer, default=0)
    last_price_update = Column(DateTime, default=func.now())
    floor_price = Column(Float, nullable=True)

class ProductSalesHistory(Base):
    __tablename__ = 'product_sales_history'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    date = Column(Date, nullable=False)
    sold_quantity = Column(Integer, default=0)
    sold_price = Column(Float, nullable=False)
    target_daily_sales = Column(Float, nullable=False)
    demand = Column(Float, nullable=False)
    floor_price = Column(Float, nullable=False)

    product = relationship(
        'Product',
        backref=backref('sales_history', lazy='select')
    )