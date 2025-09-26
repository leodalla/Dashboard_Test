# charts.py
import numpy as np
import pandas as pd
import plotly.express as px

def load_kpi_from_csv(file_or_path,scenario=None, year=None):
    """
    Reads a CSV with columns: Scenario, Year, KPI, Value.
    Filters by `scenario` and `year` if provided.
    Returns a list of dicts: [{"kpi": "...", "value": "..."}...]
    """
    df = pd.read_csv(file_or_path)

    # normalize column names -> original names
    cols = {c.strip().lower(): c for c in df.columns}

    # required columns (fallback to first two if named differently)
    k_col = cols.get("kpi")   or cols.get("name") or list(df.columns)[0]
    v_col = cols.get("value") or cols.get("val")  or list(df.columns)[1]

    #filter columns
    scen_col = cols.get("scenario")
    year_col = cols.get("year")

    # apply filters if columns exist and filter values are given
    if scen_col is not None and scenario is not None:
        df = df[df[scen_col].astype(str) == str(scenario)]
    if year_col is not None and year is not None:
        df = df[df[year_col].astype(str) == str(year)]

    # build result with value rounded to 1 decimal
    out = []
    for _, r in df[[k_col, v_col]].iterrows():
        try:
            val = float(r[v_col])
            val = f"{val:.1f}"   # format to 1 decimal place
        except (ValueError, TypeError):
            val = str(r[v_col]).strip()  # fallback if not numeric
        out.append({"kpi": str(r[k_col]).strip(), "value": val})
        
    return out