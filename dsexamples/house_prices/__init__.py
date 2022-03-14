"""
Dataset from https://www.kaggle.com/harlfoxem/housesalesprediction
"""

from dsexamples import create_path

from dslib import pandas_from_parquet


data = pandas_from_parquet(
    create_path('kc_house_data.parquet', reference=__file__).as_posix()
)
