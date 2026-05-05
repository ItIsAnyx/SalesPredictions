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
    password = Column(String(255), nullable=False)

    shops = relationship("Shop", back_populates="owner")

class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    shop_owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", foreign_keys=[shop_owner], back_populates="shops")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False)

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)

    shop = relationship("Shop")
    category = relationship("Category")
    region = relationship("Region")

class PriceHistory(Base):
    __tablename__ = "price_histories"
    __table_args__ = (Index("ix_product_time", "product_id", "changed_at"),)
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    changed_by = Column(Integer, ForeignKey('users.id'), nullable=False)

    product = relationship("Product")
    changed_by_user = relationship("User")

    # Необязательные столбцы, т. к. вряд ли пользователь станет указывать сезон, погоду и выходные,
    # но можно будет автоматически подтягивать данные с помощью каких-нибудь модулей и доп. функционала
    season = Column(String(10), nullable=True)
    weather_condition = Column(String(10), nullable=True)
    weekend = Column(Boolean, nullable=True)

# --- Подписки ---

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False) # Цена за месяц

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum("active", "expired", "cancelled", "inactive", name="subscription_status", create_type=False), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sub_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=False)

    user = relationship("User")
    sub = relationship("Subscription")