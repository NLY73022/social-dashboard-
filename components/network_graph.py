"""
network_graph.py

Builds the interactive network graph showing the structural architecture
of student digital enclaves (Topic 6, Deliverable 4a).

Nodes  = students
Edges  = interaction ties (weighted by frequency), colored by platform
Layout = spring layout via networkx, rendered with Plotly for Dash.
"""

import networkx as nx
import plotly.graph_objects as go
import pandas as pd

PLATFORM_COLORS = {
    "WhatsApp": "#25D366",
    "X (Twitter)": "#1DA1F2",
    "Instagram": "#C13584",
    "TikTok": "#010101",
}


def build_graph(edges_df: pd.DataFrame, survey_df: pd.DataFrame,
                 platform_filter: str = "All") -> go.Figure:
    """Return a Plotly figure of the student interaction network.

    Args:
        edges_df: columns [source, target, platform, weight]
        survey_df: columns include student_id, usage_mode, primary_platform
        platform_filter: "All" or one of PLATFORM_COLORS keys
    """
    df = edges_df if platform_filter == "All" else edges_df[edges_df.platform == platform_filter]

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row["source"], row["target"], weight=row["weight"], platform=row["platform"])

    if G.number_of_nodes() == 0:
        return go.Figure().update_layout(title="No edges for this filter")

    pos = nx.spring_layout(G, k=0.4, seed=42, weight="weight")

    # usage_mode lookup for node coloring (active vs passive)
    mode_lookup = survey_df.set_index("student_id")["usage_mode"].to_dict()

    # Edge traces, grouped by platform so the legend is meaningful
    edge_traces = []
    for platform, color in PLATFORM_COLORS.items():
        ex, ey = [], []
        for u, v, data in G.edges(data=True):
            if data["platform"] != platform:
                continue
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            ex += [x0, x1, None]
            ey += [y0, y1, None]
        if ex:
            edge_traces.append(go.Scatter(
                x=ex, y=ey, mode="lines",
                line=dict(width=1, color=color),
                opacity=0.5, hoverinfo="none", name=platform, showlegend=True,
            ))

    node_x, node_y, node_text, node_color = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        mode = mode_lookup.get(node, "unknown")
        node_text.append(f"{node}<br>Mode: {mode}<br>Degree: {G.degree(node)}")
        node_color.append("#019251" if mode == "active" else "#999999")

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers",
        marker=dict(size=9, color=node_color, line=dict(width=1, color="white")),
        text=node_text, hoverinfo="text", name="Students", showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title="Digital Enclave Network — active (green) vs passive (grey) students",
        showlegend=True,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
    )
    return fig
