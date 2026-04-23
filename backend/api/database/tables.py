from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, Boolean, Enum, Index
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# --- Основные экономические таблички ---

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)

    shops = relationship("Shop", back_populates="owner")

class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    shop_owner = Column(Integer, ForeignKey('user.id'), nullable=False)

    owner = relationship("User", foreign_keys=[shop_owner], back_populates="shops")

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False)

class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(64), nullable=False)

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    shop = relationship("Shop")
    category = relationship("Category")
    region = relationship("Region")

class PriceHistory(Base):
    __tablename__ = "price_history"
    __table_args__ = (Index("ix_product_time", "product_id", "changed_at"),)
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    changed_by = Column(Integer, ForeignKey('user.id'), nullable=False)

    product = relationship("Product")
    changed_by_user = relationship("User")

    # Необязательные столбцы, т. к. вряд ли пользователь станет указывать сезон, погоду и выходные,
    # но можно будет автоматически подтягивать данные с помощью каких-нибудь модулей и доп. функционала
    season = Column(String(10), nullable=True)
    weather_condition = Column(String(10), nullable=True)
    weekend = Column(Boolean, nullable=True)

# --- Подписки ---

class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False) # Цена за месяц

class PurchaseHistory(Base):
    __tablename__ = "purchase_history"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum("active", "expired", "cancelled", "inactive", name="subscription_status"), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    sub_id = Column(Integer, ForeignKey('subscription.id'), nullable=False)

    user = relationship("User")
    sub = relationship("Subscription")