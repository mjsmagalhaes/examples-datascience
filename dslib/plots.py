import numpy as np
import pandas as pd
import seaborn as sns
# import matplotlib.pyplot as plt
import altair as alt
import pydash as py

import plotly.graph_objects as go
# import plotly.express as px

# from ipywidgets import widgets, Layout
from icecream import ic


def plot_full_histogram_(
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
            texttemplate=r"%{y}"
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


def plot_full_boxplot_(data: pd.DataFrame, attrib_list=None):
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


def plot_corr_heatmap(data, size=None):
    """
    Plot correlation matrix and returns it.
    """
    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # if size is not None:
    #   f, ax = plt.subplots(figsize=size)

    sns.heatmap(corr, mask=mask, center=0, linewidth=0.5)

    return corr


class plot:
    def __init__(self, kind=None, params: dict = {}) -> None:
        self.kind = kind
        self.params = {
            'properties': {'width': 800}
        }

    def __add__(self, x):
        if isinstance(x, dict):
            self.params.update(x)
            return self
        else:
            raise(Exception('BOOM.'))

    def set(self, propType='properties', **kw):
        for k, v in kw.items():
            py.set_(self.params, propType+'.'+k, v)
        return self

    def merge(self, params: dict, default: dict = {}):
        p = py.clone_deep(self.params)
        return py.merge(default, p, params)

    def histogram(self, data: pd.DataFrame, attrib: str, params: dict = {}):
        params = self.merge(params, {
            'properties': {
                'title': '[{0}] Data Distribution'.format(attrib.upper())
            }
        })
        # ic(params)
        return alt.Chart(data).mark_bar(
            **params.get('bar', {})
        ).encode(
            alt.X(attrib, **params.get('x', {})),
            alt.Y('count()', **params.get('y', {})),
            **params.get('encode', {})
        ).properties(
            **params.get('properties', {})
        ).interactive()

    def histogram_all(
        self,
        data: pd.DataFrame,
        attrib_list=None, attrib_active_idx=0,
        params={}
    ):

        params = self.merge(params, {
            'properties': {
                'title': 'Histogram of All Variables'
            }
        })
        ic(params)

        input_dropdown = alt.binding_select(
            options=data.columns.tolist(),
            name='Variables'
        )

        selection = alt.selection_single(
            fields=['column'],
            bind=input_dropdown,
            init={'column': data.columns[0]}
        )

        return alt.Chart(data).mark_bar(**params.get('bar', {})).transform_fold(
            data.columns.tolist(),
            as_=['column', 'value']
        ).transform_filter(
            selection
        ).encode(
            x=alt.X(
                'value:N',
                title=None,
                **params.get('x', {'bin': {'maxbins': 30}})
            ),
            y=alt.Y('count():Q', **params.get('y', {})),
            column='column:N',
            **params.get('encode', {})
        ).properties(
            **params.get('properties', {})
        ).add_selection(
            selection
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_header(
            titleFontSize=14,
            labelFontSize=12
        ).interactive()

    def boxplot(self, data, x, y):
        return alt.Chart(data).mark_boxplot().encode(
            x=x, y=y
        ).interactive()

    def boxplot_all(self, data: pd.DataFrame, attrib_list=None):
        return alt.Chart(data).transform_fold(
            data.columns.tolist(),
            as_=['Variables', 'value']
        ).mark_boxplot().encode(
            x='Variables:N',
            y='value:Q',
            color=alt.Color('Variables:N')
        ).properties(
            width=1000
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=14
        ).interactive()

    def corr_heatmap(self, data: pd.DataFrame):
        corrMatrix = data.corr().reset_index().melt('index')
        corrMatrix.columns = ['var1', 'var2', 'correlation']

        chart = alt.Chart(corrMatrix).mark_rect().encode(
            x=alt.X('var1', title=None),
            y=alt.Y('var2', title=None),
            color=alt.Color('correlation', legend=None),
        ).properties(
            width=800,
            height=alt.Step(40)
        )

        chart += chart.mark_text(size=18).encode(
            text=alt.Text('correlation', format=".2f"),
            color=alt.condition(
                "datum.correlation > 0.5",
                alt.value('white'),
                alt.value('black')
            )
        )

        return chart.transform_filter("datum.var1 <= datum.var2").configure_axis(
            labelFontSize=12
        ).interactive()
