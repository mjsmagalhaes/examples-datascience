from dsexamples import create_path

from dslib import pandas_from_csv


data = pandas_from_csv(
    create_path('imports85/imports-85.csv').as_posix()
)
