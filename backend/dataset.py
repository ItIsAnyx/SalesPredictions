import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

def load_dataset(backend_key):
    print(backend_key)
    file_path = "retail_store_inventory.csv"

    df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS,
                                  "anirudhchauhan/retail-store-inventory-forecasting-dataset",
                                  file_path,)
    return df