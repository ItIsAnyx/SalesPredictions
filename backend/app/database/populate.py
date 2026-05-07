from app.database.db import SessionLocal
from app.database.models import Store, Category, Region, Product, PriceHistory, User
from app.auth.service import hash_password

def get_session():
    return SessionLocal()

# Извлечение уникальных сущностей
def extract_unique_entities(df):
    stores = df["Store"].unique()
    categories = df["Category"].unique()
    regions = df["Region"].unique()

    return stores, categories, regions

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
        last_name="User",
        password=hash_password("123123123")
    )
    session.add(user)
    session.flush()

    return user.id

def insert_stores(session, stores, user_id):
    store_map = {}
    for store in stores:
        obj = Store(title=store, user_id=user_id)
        session.add(obj)
        session.flush()
        store_map[store] = obj.id

    return store_map

# Вставка информации о продуктах
def insert_products(session, df, store_map, category_map):
    product_map = {}
    unique_products = df[["Product", "Store", "Category"]].drop_duplicates()

    for _, row in unique_products.iterrows():
        key = (row["Product"], row["Store"])
        obj = Product(
            title=row["Product"],
            store_id=store_map[row["Store"]],
            category_id=category_map[row["Category"]]
        )

        session.add(obj)
        session.flush()
        product_map[key] = obj.id

    return product_map

# Информация обо всех изменениях цен
def insert_price_history(session, df, product_map, region_map):
    objects = []

    for _, row in df.iterrows():
        key = (row["Product"], row["Store"])

        obj = PriceHistory(
            price=row["Price"],
            changed_at=row["Date"],
            product_id=product_map[key],
            region_id=region_map[row["Region"]],
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

        stores, categories, regions = extract_unique_entities(df)
        user_id = create_default_user(session)

        category_map = insert_categories(session, categories)
        print(f"Добавлено {len(category_map)} категорий продуктов")

        region_map = insert_regions(session, regions)
        print(f"Добавлено {len(region_map)} регионов")

        store_map = insert_stores(session, stores, user_id)
        print(f"Добавлено {len(store_map)} магазинов")

        product_map = insert_products(session, df, store_map, category_map)
        print(f"Добавлено {len(product_map)} продуктов")

        price_history = insert_price_history(session, df, product_map, region_map)
        print(f"Добавлено {len(price_history)} изменений цен на продукты")

        session.commit()
        print("БД успешно заполнена данными")

    except Exception as e:
        session.rollback()
        print("Ошибка во время заполнения БД данными:", e)

    finally:
        session.close()