from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, Boolean, Enum, Index
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    role = Column(
        Enum("USER", "ADMIN", name="user_roles"),
        nullable=False, default="USER"
    )
    password = Column(String(255), nullable=False)

    stores = relationship("Store", back_populates="owner")

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="stores")
    products = relationship("Product", back_populates="store")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False, unique=True)

    products = relationship("Product", back_populates="category")

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False)

    price_histories = relationship("PriceHistory", back_populates="region")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")
    price_histories = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = "price_histories"
    __table_args__ = (Index("ix_product_time", "product_id", "changed_at"),)
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    price = Column(DECIMAL(10, 2, asdecimal=True), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    season = Column(
        Enum("Spring", "Winter", "Summer", "Autumn", name="price_history_season"),
        nullable=False
    )
    weather_condition = Column(
        Enum("Sunny", "Rainy", "Snowy", "Cloudy", name="price_history_weather_condition"),
        nullable=False
    )
    weekend = Column(Boolean, nullable=True)

    product = relationship("Product", back_populates="price_histories")
    region = relationship("Region", back_populates="price_histories")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable=False)
    price = Column(DECIMAL(10, 2, asdecimal=True), nullable=False)

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(
        Enum("active", "expired", "cancelled", "inactive", name="subscription_status"),
        nullable=False
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sub_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=False)

    user = relationship("User")
    sub = relationship("Subscription")

class SubscriptionDuration(Base):
    __tablename__ = "subscription_durations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    months = Column(Integer, nullable=False, unique=True)
    multiplier = Column(DECIMAL(10, 2, asdecimal=True), nullable=False)
    label = Column(String(64), nullable=False)

    subscription = relationship("Subscription")