import pandas as pd
import random
import os
import datetime

region_price = {"North": 1.05, "East": 1.00, "West": 0.98, "South": 0.96}
category_amplitude = {"Furniture": 0.1, "Toys": 0.35, "Clothing": 0.25, "Groceries": 0.05, "Electronics": 0.15}
weather_condition = {"Rainy": 0.85, "Sunny": 1.00, "Cloudy": 0.95, "Snowy": 0.89}
inflation = 1.06

# Словари для генерации
stores = ["MegaMart", "SuperPrice", "GreenShop", "TechWorld", "HomeComfort"]

products_by_category = {
    "Groceries": [
        {"name": "Milk 1L", "initial_price": 89.99},
        {"name": "Bread", "initial_price": 45.49},
    ],
    "Toys": [
        {"name": "Lego Classic Set", "initial_price": 1299.00},
        {"name": "Barbie Doll", "initial_price": 799.00},
    ],
    "Clothing": [
        {"name": "Jeans", "initial_price": 2499.00},
        {"name": "T-shirt", "initial_price": 899.00},
    ],
    "Furniture": [
        {"name": "Office Chair", "initial_price": 5499.00},
        {"name": "Dining Table", "initial_price": 8999.00},
    ],
    "Electronics": [
        {"name": "Wireless Headphones", "initial_price": 3499.00},
        {"name": "Smartphone Charger", "initial_price": 1299.00},
    ]
}

def get_season(month):
    if month in {12, 1, 2}:
        return "Winter"
    elif month in {3, 4, 5}:
        return "Spring"
    elif month in {6, 7, 8}:
        return "Summer"
    else:
        return "Autumn"

def get_weather(season):
    weather_probs = {
        "Winter":  ["Snowy", "Cloudy", "Sunny"],
        "Spring":  ["Rainy", "Cloudy", "Sunny"],
        "Summer":  ["Sunny", "Sunny", "Cloudy", "Rainy"],
        "Autumn":  ["Rainy", "Cloudy", "Sunny"]
    }
    return random.choice(weather_probs[season])

duration_ranges = {
    "Winter": (2, 6),
    "Spring": (1, 4),
    "Summer": (3, 8),
    "Autumn": (2, 5)
}

def generate_weather_series(seasons):
    weather_list = []
    i = 0
    n = len(seasons)
    while i < n:
        season = seasons[i]
        weather = get_weather(season)
        min_d, max_d = duration_ranges[season]
        duration = random.randint(min_d, max_d)

        for _ in range(duration):
            if i >= n:
                break

            weather_list.append(weather)
            i += 1

    return weather_list

def gen_date_conditions(start, end):
    df = pd.DataFrame({
        "Date": pd.date_range(start=start, end=end, freq="D")
    })
    df["Season"] = df["Date"].dt.month.apply(get_season)
    df["Weather Condition"] = generate_weather_series(df["Season"].tolist())
    df["Weekend"] = (df["Date"].dt.weekday >= 5).astype(int)
    return df

def generate_price_series(date_df: pd.DataFrame, region: str, category: str, initial_price: float) -> pd.DataFrame:
    """
    Генерирует реалистичный временной ряд цен для товара.

    Зависимости:
    - Регион — простой фиксированный множитель (region_price).
    - Сезон — сезонность (с разной амплитудой в зависимости от category_amplitude).
    - Погода — прямой множитель из weather_condition.
    - Выходные — небольшая надбавка
    - Категория — влияет на:
        - силу сезонных колебаний,
        - частоту и размер «скачков» цены (промо/повышения).
    - Инфляция — плавный рост по дням (1.06 в год).
    - Финальный шум — ±2% каждый день.

    Возвращает: копию date_df + колонка 'Price'.
    """
    df = date_df.copy()

    # Базовая цена с учётом региона
    region_mult = region_price.get(region, 1.0)
    current_base = initial_price * region_mult
    seasonal_bases = {
        "Winter": 0.94,
        "Spring": 1.03,
        "Summer": 1.07,
        "Autumn": 0.96
    }

    # Сглаживание для более плавных переходов между сезонами
    df['RawSeasonalBase'] = df['Season'].map(lambda s: seasonal_bases.get(s, 1.0))
    df['SmoothedSeasonalBase'] = df['RawSeasonalBase'].ewm(span=40, adjust=False).mean()

    # День недели для контроля скачков
    df['Weekday'] = df['Date'].dt.weekday
    prices = []
    start_date = df['Date'].iloc[0]

    # Фиксация цены на случайное количество дней, чтобы не было постоянных резких скачков
    last_fixed_price = None
    fixed_days_remaining = 0

    for idx, row in df.iterrows():
        days_since_start = (row['Date'] - start_date).days

        if fixed_days_remaining > 0:
            final_price = last_fixed_price
            fixed_days_remaining -= 1

        else:
            # 1. Инфляция (накопительная)
            inflation_mult = inflation ** (days_since_start / 365.0)

            # 2. Сезонность (зависит от сезона + амплитуды категории)
            smoothed_base = df['SmoothedSeasonalBase'].iloc[idx]
            seasonal_factor = 1 + (smoothed_base - 1) * (0.6 + category_amplitude.get(category, 0.1))

            # 3. Погодные условия
            weather_mult = 1.0 + (weather_condition.get(row['Weather Condition'], 1.0) - 1.0) * 0.4

            # 4. Выходные (небольшая надбавка)
            weekend_mult = 1 + random.uniform(0.005, 0.02) if row['Weekend'] == 1 else 1.0

            # 5. Базовая цена дня (без скачков и шума)
            tentative_price = current_base * inflation_mult * seasonal_factor * weather_mult * weekend_mult

            # 6. Скачки цены (зависят от категории)
            # Высокая амплитуда (Toys, Clothing) → чаще и сильнее скачки
            amp = category_amplitude.get(category, 0.1)

            # Разная вероятность и сила скачков по категориям
            if category in {"Groceries", "Furniture"}:
                jump_prob = 0.0004 + amp * 0.001
                max_jump = 0.035
            elif category == "Electronics":
                jump_prob = 0.001 + amp * 0.0025
                max_jump = 0.09
            else:  # Toys, Clothing — самые волатильные
                jump_prob = 0.0016 + amp * 0.004
                max_jump = 0.11

            # Сглаживание скачков на выходных
            weekday = row['Weekday']
            if weekday >= 5:  # Пт, Сб, Вс
                jump_prob *= 0.3
            elif weekday == 4:
                jump_prob *= 0.6

            if random.random() < jump_prob:
                # Два типа скачков: мелкий частый и редкий крупный
                if random.random() < 0.75:  # 75% — мелкий скачок
                    jump_size = random.uniform(-max_jump * 0.6, max_jump * 0.6)
                else:  # 25% — крупный скачок
                    jump_size = random.uniform(-max_jump, max_jump)

                if category == "Electronics" and random.random() < 0.6:
                    jump_size = min(jump_size, 0)

                tentative_price *= (1 + jump_size)

            # 7. Случайный шум ± 0.4%
            noise = random.uniform(-0.004, 0.004)
            final_price = tentative_price * (1 + noise)

            # Цена не может быть отрицательной
            final_price = max(final_price, 0.01)

            # Фиксация цены на n дней, начиная с сегодняшнего
            last_fixed_price = final_price
            fixed_days_remaining = random.randint(2, 12) - 1
            if category in {"Groceries", "Furniture"}:
                fixed_days_remaining += random.randint(4, 10)
            elif category == "Electronics":
                fixed_days_remaining += random.randint(1, 4)

        prices.append(round(final_price, 2)) # округление до копеек

    df['Price'] = prices
    df = df.drop(columns=['RawSeasonalBase', 'SmoothedSeasonalBase', 'Weekday'], errors='ignore')
    return df

# Генерирует полный датасет для всех магазинов и товаров. Возвращает один большой DataFrame.
def generate_full_dataset(start_date: str = '2024-01-01', end_date: str = '2026-01-01') -> pd.DataFrame:
    print("Генерация календаря с погодными условиями...")
    date_df = gen_date_conditions(start_date, end_date)

    all_records = []

    print("Начинаю генерацию цен по магазинам и товарам...")

    for store in stores:
        print(f"\nОбработка магазина: {store}")

        for category, products in products_by_category.items():
            for product in products:
                print(f"Товар: {product['name']} ({category})")

                for region in region_price:
                    # Генерируем цены именно для этого товара
                    price_df = generate_price_series(
                        date_df=date_df.copy(),
                        region=region,
                        category=category,
                        initial_price=product['initial_price']
                    )

                    # Добавляем информацию о магазине и товаре
                    price_df = price_df.assign(
                        Store=store,
                        Product=product['name'],
                        Category=category,
                        Region=region,
                        InitialPrice=product['initial_price']
                    )

                    # Переставляем столбцы в удобном порядке
                    cols = ['Date', 'Store', 'Product', 'Category', 'Region', 'Price'] + \
                           [c for c in price_df.columns if
                            c not in ['Date', 'Store', 'Product', 'Category', 'Region', 'Price', 'InitialPrice']]

                    all_records.append(price_df[cols])

    # Объединяем всё в один большой датафрейм
    full_df = pd.concat(all_records, ignore_index=True)

    # Сортируем по дате и магазину/товару
    full_df = full_df.sort_values(by=['Date', 'Store', 'Product']).reset_index(drop=True)

    print(f"Генерация завершена! Итоговый размер датасета: {full_df.shape}")
    return full_df

# Сохранение в csv файл
def save_dataset(df: pd.DataFrame, filename: str = "retail_forecasting_dataset.csv"):
    df.to_csv(filename, index=False)
    print(f"Датасет успешно сохранён в файл: {filename}")

# Проверка и загрузка файла. Если файл существует — загружает его. Если нет — генерирует новый и сохраняет.
def get_or_generate_dataset(filename: str = "retail_forecasting_dataset.csv") -> pd.DataFrame:

    if os.path.exists(filename):
        print(f"Файл {filename} найден. Загружаем существующий датасет...")
        return pd.read_csv(filename, parse_dates=['Date'])
    else:
        print(f"Файл {filename} не найден. Начинаем генерацию нового датасета...")
        df = generate_full_dataset()
        save_dataset(df, filename)
        return df