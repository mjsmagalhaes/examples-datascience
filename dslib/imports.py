"""
Implement data import functions and file format conversions.

Supported formats: 
    [csv][dslib.imports.pandas_from_csv], 
    [parquet][dslib.imports.pandas_from_parquet], 
    [feather][dslib.imports.pandas_from_feather].
"""

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
    """Load a csv file to a pandas DataFrame.

        Uses pyarrow to load a csv file into a [pyarrow.Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) and convert to pandas format.

        Args:
            file (str): the csv file path.
    """
    return csv.read_csv(file).to_pandas()


def pandas_from_parquet(file: str = None) -> pd.DataFrame:
    """ Load a parquet file to a pandas DataFrame.

        Uses pyarrow to load a parquet file into a [pyarrow.Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) and convert to pandas format.

        Args:
            file (str): the parquet file path.
    """
    return parquet.read_pandas(file).to_pandas()


def pandas_from_feather(file: str = None) -> pd.DataFrame:
    """ Load a feather file to a pandas DataFrame.

        Uses pyarrow to load a csv file into a [pyarrow.Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) and convert to pandas format.

        Args:
            file (str): the feather file path.
    """
    return feather.read_feather(file).to_pandas()

# -- Conversions --


def csv_to_parquet(file: str) -> None:
    """ Convert csv files to parquet.
        Args:
            file (str): the csv file path.

        !!! warning "Todo"
            Replace file extension with the appropriate extension.
    """
    t = csv.read_csv(file+'.csv')
    parquet.write_table(t, file+'.parquet')


def csv_to_feather(file: str) -> None:
    """ Convert csv files to feather.
        Args:
            file (str): the csv file path.

        !!! warning "Todo"
            Replace file extension with the appropriate extension.
    """
    t = csv.read_csv(file+'.csv')
    feather.write_feather(t, file+'.feather')
