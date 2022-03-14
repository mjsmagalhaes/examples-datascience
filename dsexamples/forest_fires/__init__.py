"""
Dataset from https://archive.ics.uci.edu/ml/datasets/forest+fires
"""

from dsexamples import create_path

from dslib import pandas_from_parquet


data = pandas_from_parquet(
    create_path('forestfires.parquet', reference=__file__).as_posix()
)
