
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    cost_price = Column(Float)
    current_sales_price = Column(Float)

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    competitor = Column(String)
    price = Column(Float)
    collected_at = Column(DateTime, default=datetime.utcnow)

class PriceSuggestion(Base):
    __tablename__ = "price_suggestions"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    suggested_price = Column(Float)
    status = Column(String, default="Pendente")
