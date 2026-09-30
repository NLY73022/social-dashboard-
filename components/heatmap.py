"""
heatmap.py

Builds the geospatial campus heatmap overlaying self-reported digital
activity hotspots on physical campus locations (Topic 6, Deliverable 4b).
"""

import plotly.express as px
import pandas as pd


def build_heatmap(survey_df: pd.DataFrame, locations_df: pd.DataFrame) -> "px.Figure":
    """Return a density mapbox figure of digital-activity intensity by location.

    Args:
        survey_df: columns include location_id, daily_screen_time_hrs
        locations_df: columns [location_id, location_name, lat, lon]
    """
    merged = survey_df.merge(locations_df, on="location_id", how="left")

    # weight = a simple proxy for "digital intensity" at that physical spot
    agg = (
        merged.groupby(["location_id", "location_name", "lat", "lon"])
        .agg(avg_screen_time=("daily_screen_time_hrs", "mean"),
             respondent_count=("student_id", "count"))
        .reset_index()
    )

    fig = px.density_mapbox(
        agg,
        lat="lat", lon="lon",
        z="avg_screen_time",
        radius=35,
        center=dict(lat=agg["lat"].mean(), lon=agg["lon"].mean()),
        zoom=15,
        mapbox_style="open-street-map",
        hover_name="location_name",
        hover_data={"avg_screen_time": ":.1f", "respondent_count": True,
                    "lat": False, "lon": False},
        color_continuous_scale=["#e8f5e9", "#66bb6a", "#019251", "#013d20"],
        title="Digital Activity Intensity by Campus Location",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig
