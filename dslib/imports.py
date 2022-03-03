import os
import datatable as dt
import pandas as pd
# import deal


# file_must_exist = deal.chain(
#     deal.pre(lambda file: os.path.exists(file)),
#     deal.has('read')
# )


# @file_must_exist
def datatable_from_csv(file: str = None) -> dt.Frame:
    return dt.fread(file)


# @file_must_exist
def pandas_from_csv(file: str = None) -> pd.DataFrame:
    return datatable_from_csv(file).to_pandas()
