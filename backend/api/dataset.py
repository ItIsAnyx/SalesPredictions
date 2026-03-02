import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
from config import settings, validate_key

def load_dataset(backend_key):
    file_path = "retail_store_inventory.csv"

    df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS,
                                  settings.KAGGLE_DATASET,
                                  file_path,)
    return df

def dataset_preprocessing(df):
    df["Category"] = df["Category"].astype("category")
    df["Region"] = df["Region"].astype("category")
    df["Weather Condition"] = df["Weather Condition"].astype("category")
    df["Seasonality"] = df["Seasonality"].astype("category")

    return df