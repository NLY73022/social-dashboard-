"""
generate_sample_data.py

Creates placeholder CSVs shaped like the real survey output described in
Topic 6, so the dashboard can be built and tested before real data comes in.

Replace these files with real exports from your survey tool (Google Forms,
KoboToolbox, Qualtrics, etc.) once data collection is done. Keep the same
column names and the dashboard will work without changes.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# ---------------------------------------------------------------------
# 1. locations.csv — campus locations students can be geotagged to.
#    Replace lat/long with real coordinates for your campus.
# ---------------------------------------------------------------------
locations = pd.DataFrame({
    "location_id": range(1, 9),
    "location_name": [
        "Main Library", "Hostel A Common Room", "Hostel B Common Room",
        "Lecture Hall 1", "Lecture Hall 2", "Central Cafeteria",
        "Sports Grounds", "Student Union Building"
    ],
    "lat": [0.3327, 0.3355, 0.3340, 0.3320, 0.3315, 0.3330, 0.3300, 0.3345],
    "lon": [32.5675, 32.5690, 32.5700, 32.5670, 32.5665, 32.5680, 32.5650, 32.5695],
})
locations.to_csv("/home/claude/social_dashboard/data/locations.csv", index=False)

# ---------------------------------------------------------------------
# 2. survey_data.csv — one row per student respondent.
#    platform_mode: "active" (posting/producing) vs "passive" (scrolling/consuming)
#    loneliness_score: UCLA Loneliness Scale (20-80)
#    dass21_score: DASS-21 total (0-63)
# ---------------------------------------------------------------------
n = 120
platforms = ["WhatsApp", "X (Twitter)", "Instagram", "TikTok"]
modes = ["active", "passive"]

survey = pd.DataFrame({
    "student_id": [f"S{1000+i}" for i in range(n)],
    "location_id": np.random.choice(locations["location_id"], n),
    "primary_platform": np.random.choice(platforms, n, p=[0.35, 0.15, 0.30, 0.20]),
    "usage_mode": np.random.choice(modes, n, p=[0.4, 0.6]),
    "daily_screen_time_hrs": np.round(np.random.gamma(4, 1.1, n), 1),
    "loneliness_score": np.random.randint(20, 80, n),
    "dass21_score": np.random.randint(0, 63, n),
    "isolation_flag": np.random.choice([0, 1], n, p=[0.75, 0.25]),
})
survey.to_csv("/home/claude/social_dashboard/data/survey_data.csv", index=False)

# ---------------------------------------------------------------------
# 3. network_edges.csv — pairwise ties for the digital enclave graph.
#    Represents "who interacts with whom" within a platform/group.
#    weight = interaction frequency (e.g., messages/wk, tags, replies).
# ---------------------------------------------------------------------
edges = []
student_ids = survey["student_id"].tolist()
for i in range(250):
    a, b = np.random.choice(student_ids, 2, replace=False)
    platform = np.random.choice(platforms)
    weight = np.random.randint(1, 15)
    edges.append((a, b, platform, weight))

edges_df = pd.DataFrame(edges, columns=["source", "target", "platform", "weight"])
edges_df.to_csv("/home/claude/social_dashboard/data/network_edges.csv", index=False)

print("Sample data written to /home/claude/social_dashboard/data/")
print(f"  locations.csv     -> {len(locations)} rows")
print(f"  survey_data.csv   -> {len(survey)} rows")
print(f"  network_edges.csv -> {len(edges_df)} rows")
