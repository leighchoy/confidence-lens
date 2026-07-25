import plotly.graph_objects as go

def price_chart(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["price"],
        )
    )
    return fig