from database.db import SessionLocal
from database.tables import Shop, Category, Region, Product, PriceHistory, User
import pandas as pd

def get_session():
    return SessionLocal()

# Извлечение уникальных сущностей
def extract_unique_entities(df):
    shops = df["Store"].unique()
    categories = df["Category"].unique()
    regions = df["Region"].unique()

    return shops, categories, regions

# Вставка категорий товаров, регионов и магазинов
def insert_categories(session, categories):
    category_map = {}

    for category in categories:
        obj = Category(title=category)
        session.add(obj)
        session.flush()

        category_map[category] = obj.id

    return category_map

def insert_regions(session, regions):
    region_map = {}

    for region in regions:
        obj = Region(title=region)
        session.add(obj)
        session.flush()

        region_map[region] = obj.id

    return region_map

# Default User, которому будут присвоены все магазины
def create_default_user(session):
    user = session.query(User).filter_by(login="test").first()
    if user:
        return user.id

    user = User(
        email="test@test.com",
        login="test",
        first_name="Test",
        second_name="User"
    )
    session.add(user)
    session.flush()

    return user.id

def insert_shops(session, shops, user_id):
    shop_map = {}
    for shop in shops:
        obj = Shop(title=shop, shop_owner=user_id)
        session.add(obj)
        session.flush()
        shop_map[shop] = obj.id

    return shop_map

# Вставка информации о продуктах
def insert_products(session, df, shop_map, category_map, region_map):
    product_map = {}
    unique_products = df[["Product", "Store", "Category", "Region"]].drop_duplicates()

    for _, row in unique_products.iterrows():
        key = (row["Product"], row["Store"], row["Region"])
        obj = Product(
            title=row["Product"],
            shop_id=shop_map[row["Store"]],
            category_id=category_map[row["Category"]],
            region_id=region_map[row["Region"]],
        )

        session.add(obj)
        session.flush()
        product_map[key] = obj.id

    return product_map

# Информация обо всех изменениях цен
def insert_price_history(session, df, product_map, user_id):
    objects = []

    for _, row in df.iterrows():
        key = (row["Product"], row["Store"], row["Region"])

        obj = PriceHistory(
            price=row["Price"],
            changed_at=row["Date"],
            product_id=product_map[key],
            changed_by=user_id,
            season=row["Season"],
            weather_condition=row["Weather Condition"],
            weekend=row["Weekend"],
        )

        objects.append(obj)

    session.bulk_save_objects(objects)
    return objects


# ===== Основная функция для заполнения БД =====
def populate_db(df):
    session = get_session()

    try:
        if session.query(PriceHistory.id).first() is None:
            print("\nЗаполнение базы данных...")
        else:
            print("\nБД уже заполнена данными!")
            session.close()
            return

        shops, categories, regions = extract_unique_entities(df)
        user_id = create_default_user(session)

        category_map = insert_categories(session, categories)
        print(f"Добавлено {len(category_map)} категорий продуктов")

        region_map = insert_regions(session, regions)
        print(f"Добавлено {len(region_map)} регионов")

        shop_map = insert_shops(session, shops, user_id)
        print(f"Добавлено {len(shop_map)} магазинов")

        product_map = insert_products(session, df, shop_map, category_map, region_map)
        print(f"Добавлено {len(product_map)} продуктов")

        price_history = insert_price_history(session, df, product_map, user_id)
        print(f"Добавлено {len(price_history)} изменений цен на продукты")

        session.commit()
        print("БД успешно заполнена данными")

    except Exception as e:
        session.rollback()
        print("Ошибка во время заполнения БД данными:", e)

    finally:
        session.close()