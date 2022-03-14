"""
Implement import functions.

Supported formats: csv, parquet, feather.
"""

import os
import pandas as pd

from pyarrow import feather, parquet, csv

# import deal


# file_must_exist = deal.chain(
#     deal.pre(lambda file: os.path.exists(file)),
#     deal.has('read')
# )


# @file_must_exist
# def datatable_from_csv(file: str = None) -> dt.Frame:
#     return dt.fread(file)


# @file_must_exist
# def pandas_from_csv(file: str = None) -> pd.DataFrame:
#     return datatable_from_csv(file).to_pandas()


# @file_must_exist
def pandas_from_csv(file: str = None) -> pd.DataFrame:
    return csv.read_csv(file).to_pandas()


def pandas_from_parquet(file: str = None) -> pd.DataFrame:
    return parquet.read_pandas(file).to_pandas()


def pandas_from_feather(file: str = None) -> pd.DataFrame:
    return feather.read_feather(file).to_pandas()

# -- Conversions --


def csv_to_parquet(file: str) -> None:
    t = csv.read_csv(file+'.csv')
    parquet.write_table(t, file+'.parquet')


def csv_to_feather(file: str) -> None:
    t = csv.read_csv(file+'.csv')
    feather.write_feather(t, file+'.feather')
