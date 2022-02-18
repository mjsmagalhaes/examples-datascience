import pandas as pd

from ipywidgets import widgets, Layout


def describe_numerical(data):
  """
  Describe numerical variables printing basic statistics like: max, min, count, ...
  """
  return data.describe()


def describe_category(data):
  return data.describe(include=['object'])


def describe_category_values(data, dtype=['object', 'category']):
  """
  Describe categorical variables by printing the amount of samples each value had.
  """
  wdg_list = []
  for name, col in data.select_dtypes(include=dtype).iteritems():
    df = pd.DataFrame(col.value_counts(), columns=[name])
    wdg_list.append(
        widgets.HTML(df.to_html())
    )

  box_layout = Layout(
      display='flex',
      flex_flow='row',
      justify_content='space-around',
      width='auto'
  )

  return widgets.HBox(wdg_list, layout=box_layout)
