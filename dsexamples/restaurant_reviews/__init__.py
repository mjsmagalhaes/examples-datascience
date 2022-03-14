"""
Dataset from https://www.kaggle.com/d4rklucif3r/restaurant-reviews
"""

from dsexamples import create_path

from dslib import pandas_from_parquet


data = pandas_from_parquet(
    create_path('forestfires.parquet', reference=__file__).as_posix()
)
