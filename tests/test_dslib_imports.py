# import pytest

from dslib.imports import pandas_from_csv, datatable_from_csv

import os
import deal
from hypothesis.strategies import sampled_from


def list_files(dir='data', ext='.csv'):
  path = os.walk(dir)
  file_list = []
  for root, directories, files in path:
    # for directory in directories:
    #     print(directory)

    for file in files:
      _, fileExt = os.path.splitext(file)
      if fileExt == ext:
        file_list.append(os.path.join(root, file))

  return file_list


existing_file = sampled_from(list_files())


test_deal_pandas = deal.cases(
    pandas_from_csv,
    kwargs=dict(file=existing_file)
)

test_deal_datatable = deal.cases(
    datatable_from_csv,
    kwargs=dict(file=existing_file)
)
