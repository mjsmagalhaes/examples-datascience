import os.path as path

from pathlib import Path
from dslib.helpers import replace_csv_header
from .helpers import create_path

from dslib import pandas_from_csv


def cars85():
    csv = create_path('files/imports-85.csv')
    return pandas_from_csv(csv.as_posix())
