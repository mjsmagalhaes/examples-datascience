import numpy as np

from IPython.display import display
from ipywidgets import Output


def list_missing_values(df):
  df.replace('?', np.nan, inplace=True)

  missing_data = df.isna()
  for column in missing_data.columns:
    v = missing_data[column].value_counts()
    c = v.loc[True] if True in v.index else 0
    if c > 0:
      print('{0}: {1} missing values of type {2}'.format(
          column, c, df[column].dtypes)
      )
