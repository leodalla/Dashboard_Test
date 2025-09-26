# -*- coding: utf-8 -*-
"""
IRENA-style dashboard (test version with random plots)
Author: @Leonardo Dalla Riva
"""
import streamlit as st
from charts import random_boxplot, random_bar, random_pie 
from kpi import load_kpi_from_csv
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# Page & Theming
# =========================
st.set_page_config(page_title="IRENA Dashboard", layout="wide")

st.markdown("""
<style>
/* Sticky blue headbar */
.app-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 58px;
  background: #ffffff; /* white */
  color: #2b72c4; /* blue */
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 18px;
  z-index: 1000;
  border-bottom: 1px solid rgba(255,255,255,0.15);
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.app-header .brand { font-weight: 700; letter-spacing: .5px; font-size: 28px; }
.app-header .right { font-weight: 600; opacity: .95; }

/*constrain the logo size */
.app-header img {
  height: 40px;   /* try 32–40px for header height 58px */
  width: auto;
  object-fit: contain;
}

/* Push content below headbar */
[data-testid="stAppViewContainer"] { padding-top: 58px; background-color: #F2F3F5; }
  

/* Sidebar */
section[data-testid="stSidebar"] {
  background-color: #0D1D36; color: #fff; font-size: 38px; height: 100vh; display: flex; flex-direction: column;
}
section[data-testid="stSidebar"] * { color: #fff !important; }

/* Sidebar title ("Filters") */
section[data-testid="stSidebar"] h1 {
    font-size: 38px !important;
}

/The widget label above the radio (e.g., "Scenario Selection") */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] > div,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  font-size: 18px !important;      /* adjust size */
  font-weight: 700 !important;
}

/* KPI tiles */
.kpi {
  background: #2b3b4d; border-radius: 12px; padding: 16px 16px; color: #fff;
  border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 1px 6px rgba(0,0,0,0.25);
  height:120px;                   /* fixed tile height */
  display:flex; flex-direction:column; justify-content:center;
  text-align:left;
  margin-bottom: 16px;
}
.kpi h3 { font-size: 16px; font-weight: 600; margin: 0 0 6px 0; color:#d9e2ec;
  /* clamp to 2 lines so long titles don't push height */
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
  overflow:hidden;}
.kpi .val { font-size: 28px; font-weight: 800; line-height: 1.1; }
.kpi .sub { font-size: 12px; opacity: .8; }

/* Plotly transparent backgrounds */
.js-plotly-plot, .plotly, .stPlotlyChart { background: transparent !important; }
</style>

<div class="app-header">
  <div class="brand">IRENA - Test Dashboard</div>
  <img src="https://www.irena.org/-/media/Examples/Irena/Images/Navigation/IRENA_logo.svg?la=en&hash=C68751AAB97C5A6B6714D109A3BAC560">
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar (filters)
# =========================
with st.sidebar:
    st.title("Filters")

    scenarios_filter = st.radio(label="Scenario Selection",options=["PES", "TES", "DES"],
        horizontal=True,key="Scenario")
    years_filter = st.radio(label="Years Selection",options=["2030", "2040", "2050"],
        horizontal=True,key="years")
    ev_percent = st.slider("Percentage of households (0-20)", 0.0, 20.0, 2.5, step=0.5)
    max_loading = st.slider("Filter 1", 50, 200, 100, step=5)
    min_voltage = st.slider("Filter 2", 0.7, 1.0, 0.9, step=0.01)
    max_voltage = st.slider("Filter 3", 1.0, 1.2, 1.05, step=0.01)

# =========================
# KPI Tiles
# =========================

kpi_path="Kpi_data.csv"

kpi_data=load_kpi_from_csv(kpi_path, scenarios_filter, years_filter)
n = len(kpi_data)
max_per_row=4

# if number divides evenly, just split by max_per_row
if n % max_per_row == 0:
    row_sizes = [max_per_row] * (n // max_per_row)
else:
    # otherwise: fill first row to max_per_row,
    # and put the rest into the second row
    if n > max_per_row:
        row_sizes = [max_per_row, n - max_per_row]
    else:
        # if fewer than max_per_row, all in one row
        row_sizes = [n]
idx=0
for size in row_sizes:
    cols = st.columns(size)
    for col in cols:
        item = kpi_data[idx]
        with col:
            st.markdown(f"""
            <div class="kpi">
                <h3>{item['kpi']}</h3>
                <div class="val">{item['value']}</div>
            </div>
            """, unsafe_allow_html=True)
        idx += 1

# =========================
# Random Test Plots
# =========================

c1, c2, c3 = st.columns(3)
with c1:
    st.plotly_chart(random_boxplot("Box Plot 1", "Percentage [%]"), use_container_width=True)
with c2:
    st.plotly_chart(random_boxplot("Box Plot 2", "Unit [p.u.]"), use_container_width=True)
with c3:
    st.plotly_chart(random_pie("Pie Chart"), use_container_width=True)

# =========================
# Bottom row: two spaces for bar charts or images
# =========================

b1, b2 = st.columns(2)
with b1:
    st.subheader("Placeholder Graph 1)")
    st.plotly_chart(random_bar("Graph 1"), use_container_width=True)
    # To use an image instead later:
    # st.image("path/to/image1.png", use_container_width=True)
with b2:
    st.subheader("Placeholder Graph 2")
    st.plotly_chart(random_bar("Graph 2"), use_container_width=True)
    # To use an image instead later:
    # st.image("path/to/image2.png", use_container_width=True)