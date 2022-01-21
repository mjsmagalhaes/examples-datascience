# import numpy as np
import pandas as pd
# import altair as alt

import plotly.graph_objects as go
# import plotly.express as px


class Plot:
    def histogram(
        self,
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
                    {"title": "Attrib: " + attrib}
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

    def boxplot(self, data: pd.DataFrame, attrib_list=None):
        if attrib_list is None:
            attrib_list = data.columns

        fig = go.Figure()

        for attrib in attrib_list:
            fig.add_trace(go.Box(y=data[attrib], name=attrib))

        fig.show()