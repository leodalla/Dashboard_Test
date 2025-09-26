# charts.py
import numpy as np
import pandas as pd
import plotly.express as px

def random_boxplot(title: str, y_label: str, n_per_level: int = 24):
    """Return a Plotly boxplot figure with random data."""
    rng = np.random.default_rng(42)
    levels = [2.5, 5, 7.5, 10, 12.5, 15]
    df = pd.DataFrame({
        "EV Penetration": np.repeat(levels, n_per_level),
        y_label: rng.normal(loc=100, scale=15, size=len(levels)*n_per_level)
    })
    fig = px.box(df, x="EV Penetration", y=y_label, color="EV Penetration", title=title)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False,
        height=400
    )
    return fig

def random_bar(title: str, n: int = 5):
    """Return a Plotly bar figure with random data."""
    rng = np.random.default_rng(7)
    items = [f"Elm {i}" for i in range(1, n+1)]
    vals = rng.uniform(0.5, 1.0, size=n)
    df = pd.DataFrame({"Element": items, "Score": vals})
    fig = px.bar(df, x="Element", y="Score", title=title, text_auto=".2f")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False,
        height=520,
        margin=dict(t=50, r=20, l=20, b=40)
    )
    return fig

def random_pie(title: str, n: int = 5):
    """Return a Plotly pie chart figure with random data."""
    rng = np.random.default_rng(7)
    items = [f"Cat {i}" for i in range(1, n+1)]
    vals = rng.uniform(1, 10, size=n)  # make sure values are positive

    df = pd.DataFrame({"Category": items, "Value": vals})

    fig = px.pie(
        df,
        names="Category",
        values="Value",
        title=title,
        hole=0.3,  # donut style; remove if you want a full pie
    )

    fig.update_traces(textinfo="percent+label", textfont_size=14)

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=520,
        margin=dict(t=50, r=20, l=20, b=40),
        showlegend=True,
    )

    return fig