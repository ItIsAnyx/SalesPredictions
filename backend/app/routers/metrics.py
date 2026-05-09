from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db import get_db
from app.auth.service import get_current_user
import pandas as pd
from datetime import datetime

router = APIRouter()

"""
Поиск конкурентов для заданного товара в заданном регионе
Возвращает:
[
  {
    "product": "",
    "store": "",
    "region": "",
    "price": float,
    "changed_at": "2025-01-10"
  },
  ...
]
"""
@router.get("/{product_id}/competitors")
def get_competitors(
    product_id: int,
    region_id: int = Query(default=1),
    db: Session = Depends(get_db)
    ):
    data_query = text("""
        SELECT
            p.title AS product,
            s.title AS store,
            r.title AS region,
            ph.price,
            ph.changed_at

        FROM products p

        JOIN stores s
            ON p.store_id = s.id

        JOIN categories c
            ON p.category_id = c.id

        JOIN price_histories ph
            ON p.id = ph.product_id

        JOIN regions r
            ON ph.region_id = r.id

        WHERE p.category_id = (
            SELECT category_id
            FROM products
            WHERE id = :product_id
        )

        AND p.id != :product_id
        AND ph.region_id = :region_id

        AND ph.changed_at = (
            SELECT MAX(ph2.changed_at)
            FROM price_histories ph2
            WHERE ph2.product_id = p.id
            AND ph2.region_id = :region_id
        )

        ORDER BY ph.price ASC
    """)

    competitors = db.execute(
        data_query,
        {
            "product_id": product_id,
            "region_id": region_id
        }
    ).mappings().all()

    return competitors

"""
Подсчёт метрик для рекомендаций ценообразования
Возвращает:
{
    "competitors_found": количество конкурентов,
    "min_price": минимальная цена у конкуретов,
    "max_price": максимальная цена у конкурентов,
    "penetration_price": стратегия проникновения = min_price*0.95,
    "median_price": медианная цена,
    "premium_price": стратегия снятия сливок = max_price*1.05
}
"""
@router.get("/{product_id}/competitors_metrics")
def get_competitors_metrics(
    product_id: int,
    region_id: int = Query(default=1),
    db: Session = Depends(get_db)
    ):
    competitors = pd.DataFrame(get_competitors(product_id, region_id, db))
    if competitors.empty:
        return {
            "message": "No competitors found",
        }

    competitors["price"] = competitors["price"].astype(float)

    # Количество конкурентов, минимальная и максимальная цена у конкурентов
    competitors_found = len(competitors)
    min_price = competitors["price"].min()
    max_price = competitors["price"].max()

    # Стратегии ценообразования
    # 1. Стратегия проникновения - намеренно низкая цена для быстрого захвата рынка
    penetration_price = round(min_price * 0.95, 2)

    # 2. Нейтральное ценообразование - просто медиана
    median_price = competitors["price"].median()

    # 3. Снятие сливок - цена выше максимума на рынке. Подходит, если товар качественный и мало конкурентов
    premium_price = round(max_price * 1.05, 2)
    return {
        "competitors_found": competitors_found,
        "min_price": min_price,
        "max_price": max_price,
        "penetration_price": penetration_price,
        "median_price": median_price,
        "premium_price": premium_price
    }

"""
Посмотреть активность магазина за определённый временной период
Возвращает:
{
  "shop_id": 1,
  "period": {
    "date_start": "2026-01-01T00:00:00",
    "date_end": "2026-06-06T00:00:00"
  },
  "activities_found": 5000,
  "season_statistics": {
    "winter": 2360,
    "spring": 2640,
    "summer": 0,
    "autumn": 0
  },
  "activities": [
    {
      "changed_at": "2026-05-05T00:00:00+00:00",
      "price": 11121.7,
      "product_title": "Dining Table",
      "season": "Spring",
      "region": "North"
    },
    ...
  ]
"""
@router.get("/{shop_id}/activity")
def get_shop_activity(
    shop_id: int,
    date_start: datetime,
    date_end: datetime,
    db: Session = Depends(get_db)
):
    data_query = text("""
        SELECT
            ph.changed_at,
            ph.season,
            p.title AS product_title,
            ph.price,
            r.title as region_title
        FROM price_histories ph
        JOIN products p
            ON ph.product_id = p.id
        JOIN regions r
            ON ph.region_id = r.id
        WHERE
            p.store_id = :shop_id
            AND ph.changed_at BETWEEN :date_start AND :date_end
        ORDER BY ph.changed_at DESC
    """)

    activity_data = db.execute(
        data_query,
        {
            "shop_id": shop_id,
            "date_start": date_start,
            "date_end": date_end
        }
    ).mappings().all()

    activity_df = pd.DataFrame(activity_data)

    if activity_df.empty:
        return {"message": "No activities found"}

    # Количество всех изменений
    activities_found = len(activity_df)

    # Количество изменений по сезонам
    winter_activities = len(
        activity_df[activity_df["season"] == "Winter"]
    )

    spring_activities = len(
        activity_df[activity_df["season"] == "Spring"]
    )

    summer_activities = len(
        activity_df[activity_df["season"] == "Summer"]
    )

    autumn_activities = len(
        activity_df[activity_df["season"] == "Autumn"]
    )

    return {
        "shop_id": shop_id,
        "period": {
            "date_start": date_start,
            "date_end": date_end
        },
        "activities_found": activities_found,
        "season_statistics": {
            "winter": winter_activities,
            "spring": spring_activities,
            "summer": summer_activities,
            "autumn": autumn_activities
        },
        "activities": activity_df.to_dict(orient="records") # Сами записи активностей (Мб будет полезно для вывода графиков)
    }