import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta
from app.database.dataset import get_season, get_weather

FEATURE_COLUMNS = ["season", "weather_condition", "weekend"]
cat_features = ["season", "weekend", "weather_condition"]

cat_boost_model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    loss_function='MAE',
    verbose=100
)

def train_predict_model(df, range_days=7, is_debugging=False, model=cat_boost_model):
    dates = df['changed_at']
    print("\n\ntrain_predict_model")
    print(df.head())
    print(df.tail())
    x = df[FEATURE_COLUMNS]
    y = df['price']

    # Для проверки MAE на уже произошедших изменениях
    if is_debugging:
        train_size = len(x) - range_days

        X_train, X_test, y_train, y_test = x[:train_size], x[train_size:], y[:train_size], y[train_size:]
        dates_test = dates[train_size:]
        model.fit(X_train, y_train, cat_features=cat_features)

        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        print({"timestamp": dates_test.dt.strftime("%d-%m-%Y %H:%M:%S").tolist(), "predictions": predictions.tolist(), "mae": mae})
        return {"timestamp": dates_test.dt.strftime("%d-%m-%Y %H:%M:%S").tolist(), "predictions": predictions.tolist(), "mae": mae}

    # Для предсказаний будущего
    else:
        model.fit(x, y, cat_features=cat_features)

        x_test = get_future_x(range_days)
        predictions = model.predict(x_test.drop('changed_at', axis=1))

        print({"timestamp": x_test["changed_at"].dt.strftime("%d-%m-%Y %H:%M:%S").tolist(), "predictions": predictions.tolist(), "mae": None})
        return {"timestamp": x_test["changed_at"].dt.strftime("%d-%m-%Y %H:%M:%S").tolist(), "predictions": predictions.tolist(), "mae": None}

def get_future_x(days):
    now = datetime.now()
    result = {
        "changed_at": [now + timedelta(days=x) for x in range(1, days + 1)],
        "season": [get_season((now + timedelta(days=x)).month) for x in range(1, days + 1)],
        "weekend": [1 if (now + timedelta(days=x)).weekday() in {5, 6} else 0 for x in range(1, days + 1)]
    }
    result["weather_condition"] = get_future_weather(result["season"])

    return pd.DataFrame(result)

# Заглушка, в будущем можно реализовать подключение по API к сайтам с прогнозом погоды
def get_future_weather(condition):
    return [get_weather(a) for a in condition]