import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

import plotly.graph_objects as go
# import plotly.express as px

# from ipywidgets import widgets, Layout


def histogram_all(
    data: pd.DataFrame,
    attrib_list=None, attrib_active_idx=0
):
  if attrib_list is None:
    attrib_list = data.columns

  # Create figure
  fig = go.Figure()

  for attrib in attrib_list:
    fig.add_trace(go.Histogram(
        visible=[False, True][attrib == attrib_list[attrib_active_idx]],
        x=data[attrib],
        # name=attrib + " = %{y}",
        hoverinfo="y",
        texttemplate="%{y}"
    ))

  # Create and add slider
  steps = []
  for i, attrib in enumerate(attrib_list):
    step = dict(
        method="update",
        args=[
            {"visible": [False] * len(fig.data)},
            {"title": "[{0}] Data Distribution".format(attrib.upper())}
        ],  # layout attribute
        label=attrib,
    )
    # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i] = True
    steps.append(step)

  sliders = [dict(
      active=attrib_active_idx,
      currentvalue={
          "prefix": "Attributes: ",
          "visible": True
      },
      # pad={"t": 50},
      steps=steps
  )]

  fig.update_layout(
      sliders=sliders
  )

  fig.show()


def histogram(data, attrib, params={}):
  return alt.Chart(data).mark_bar(
      **params.get('bar', {})
  ).encode(
      alt.X(attrib, **params.get('x', {})),
      alt.Y('count()', **params.get('y', {})),
      **params.get('encode', {})
  ).properties(
      **params.get('properties', {
          'title': '[{0}] Data Distribution'.format(attrib.upper())
      })
  )


def boxplot_all(data: pd.DataFrame, attrib_list=None):
  """
  Plot boxplot for all variables.

  Expects variables to be numerical.
  """

  if attrib_list is None:
    attrib_list = data.columns

  fig = go.Figure()

  for attrib in attrib_list:
    fig.add_trace(go.Box(y=data[attrib], name=attrib))

  fig.show()


def boxplot(data, x, y):
  return alt.Chart(data).mark_boxplot().encode(
      x=x, y=y
  )


def corr(data, size=None):
  """
  Plot correlation matrix and returns it.
  """
  corr = data.corr()
  mask = np.triu(np.ones_like(corr, dtype=bool))

  if size is not None:
    f, ax = plt.subplots(figsize=size)

  sns.heatmap(corr, mask=mask, center=0, linewidth=0.5)

  return corr
