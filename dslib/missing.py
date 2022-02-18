import numpy as np
import pandas as pd

from IPython.display import display, Markdown as md


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


def missing_data(data):
  # m = np.sum(data.isna(), axis=0) + np.sum(data.isnull(), axis=0)
  m = np.sum(data.isna(), axis=0)
  s = pd.DataFrame(m, columns=['NA or Null'])
  return md(s.to_markdown())
