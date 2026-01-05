import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

file_path = "retail_store_inventory.csv"

df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS,
                              "anirudhchauhan/retail-store-inventory-forecasting-dataset",
                              file_path,)

print("Первые 5 столбцов:", df.head())