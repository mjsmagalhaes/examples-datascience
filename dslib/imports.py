import datatable as dt


def datatable_from_csv(file):
  return dt.fread(file)


def pandas_from_csv(file):
  return datatable_from_csv(file).to_pandas()
