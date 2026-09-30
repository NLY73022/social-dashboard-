"""
app.py — Social Media Spaces for University Students
Interactive Social Network & Spatial Regression Dashboard (Topic 6, Deliverable 4)

Run with:
    python app.py
Then open http://127.0.0.1:8050 in a browser.

Swap the CSVs in /data with real survey exports (same column names) once
data collection is complete — no code changes needed.
"""

from dash import Dash, html, dcc, Input, Output
import pandas as pd

from components.network_graph import build_graph, PLATFORM_COLORS
from components.heatmap import build_heatmap

# ---------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------
survey_df = pd.read_csv("data/survey_data.csv")
locations_df = pd.read_csv("data/locations.csv")
edges_df = pd.read_csv("data/network_edges.csv")

BRAND_GREEN = "#019251"
BRAND_BLACK = "#000000"

# ---------------------------------------------------------------------
# App
# ---------------------------------------------------------------------
app = Dash(__name__)
app.title = "Digital Campus Dashboard"

def stat_card(label, value):
    return html.Div(
        [
            html.Div(str(value), style={"fontSize": "28px", "fontWeight": "700", "color": BRAND_GREEN}),
            html.Div(label, style={"fontSize": "13px", "color": "#555"}),
        ],
        style={
            "backgroundColor": "white", "borderRadius": "10px", "padding": "16px 20px",
            "boxShadow": "0 1px 4px rgba(0,0,0,0.12)", "textAlign": "center", "flex": "1",
        },
    )

app.layout = html.Div(
    style={"backgroundColor": "#f4f6f5", "minHeight": "100vh", "fontFamily": "Helvetica, Arial, sans-serif"},
    children=[
        # Header
        html.Div(
            style={"backgroundColor": BRAND_BLACK, "padding": "20px 30px"},
            children=[
                html.H2("The Digital Campus: Algorithmic Enclaves, Social Comparison, "
                        "and the Hybrid Spatialities of Student Life in Kampala",
                        style={"color": "white", "margin": 0, "fontSize": "20px"}),
                html.P("Topic 6 — Interactive Social Network & Spatial Regression Dashboard",
                       style={"color": BRAND_GREEN, "margin": "4px 0 0 0", "fontSize": "14px"}),
            ],
        ),

        # Summary stat cards
        html.Div(
            style={"display": "flex", "gap": "16px", "padding": "20px 30px 0 30px"},
            children=[
                stat_card("Respondents", len(survey_df)),
                stat_card("Campus Locations", len(locations_df)),
                stat_card("Interaction Ties", len(edges_df)),
                stat_card("Avg. Daily Screen Time (hrs)", round(survey_df["daily_screen_time_hrs"].mean(), 1)),
                stat_card("% Flagged Isolation Risk", f'{round(survey_df["isolation_flag"].mean()*100)}%'),
            ],
        ),

        # Controls
        html.Div(
            style={"padding": "20px 30px 0 30px"},
            children=[
                html.Label("Filter network by platform:", style={"fontWeight": "600", "marginRight": "10px"}),
                dcc.Dropdown(
                    id="platform-filter",
                    options=[{"label": "All platforms", "value": "All"}] +
                            [{"label": p, "value": p} for p in PLATFORM_COLORS],
                    value="All",
                    clearable=False,
                    style={"width": "300px"},
                ),
            ],
        ),

        # Tabs: network graph / heatmap
        html.Div(
            style={"padding": "20px 30px"},
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="network",
                    children=[
                        dcc.Tab(label="Network Graph — Digital Enclaves", value="network"),
                        dcc.Tab(label="Geospatial Heatmap — Physical Campus", value="heatmap"),
                    ],
                    style={"marginBottom": "10px"},
                ),
                dcc.Graph(id="main-graph", style={"height": "70vh"}),
            ],
        ),
    ],
)


@app.callback(
    Output("main-graph", "figure"),
    Input("tabs", "value"),
    Input("platform-filter", "value"),
)
def update_graph(tab, platform_filter):
    if tab == "network":
        return build_graph(edges_df, survey_df, platform_filter)
    return build_heatmap(survey_df, locations_df)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
