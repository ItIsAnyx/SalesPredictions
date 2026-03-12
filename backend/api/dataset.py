import pandas as pd
import random
from config import validate_key

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

def gen_date_conditions(backend_key, start, end):
    validate_key(backend_key)
    df = pd.DataFrame({
        "Date": pd.date_range(start=start, end=end, freq="D")
    })
    df["Season"] = df["Date"].dt.month.apply(get_season)
    df["Weather Condition"] = generate_weather_series(df["Season"].tolist())
    df["Weekend"] = (df["Date"].dt.weekday >= 5).astype(int)
    return df