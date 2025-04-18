import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")
st.title("🎯 Player Group Transitions")

# All player value groups and their associated colors
all_groups = ["low", "medium", "high", "pvip", "vip", "svip"]
group_colors = {
    "low": "#A6CEE3",
    "medium": "#1F78B4",
    "high": "#33A02C",
    "pvip": "#FB9A99",
    "vip": "#E31A1C",
    "svip": "#FF7F00"
}

# Sidebar: select groups separately for source and target
source_groups = st.sidebar.multiselect(
    "Select source groups (BEFORE):",
    options=all_groups,
    default=all_groups
)

target_groups = st.sidebar.multiselect(
    "Select target groups (AFTER):",
    options=all_groups,
    default=all_groups
)

# Validation
if not source_groups or not target_groups:
    st.warning("Please select at least one group for both BEFORE and AFTER.")
    st.stop()

# Generate random transitions between all possible group pairs
transitions = []
for from_group in all_groups:
    for to_group in all_groups:
        transitions.append({
            "source": from_group,
            "target": to_group,
            "value": random.randint(20, 100)
        })

# Filter transitions based on selected groups
filtered_transitions = [
    t for t in transitions if t["source"] in source_groups and t["target"] in target_groups
]

# Define node labels
source_labels = [g + "_before" for g in source_groups]
target_labels = [g + "_after" for g in target_groups]
label_names = source_labels + target_labels

# Map labels to Sankey node indices
label_to_index = {label: idx for idx, label in enumerate(label_names)}

# Define node colors
node_colors = [group_colors[g] for g in source_groups] + [group_colors[g] for g in target_groups]

# Prepare data for Sankey diagram
sources = []
targets = []
values = []
link_colors = []

for t in filtered_transitions:
    src_label = t["source"] + "_before"
    tgt_label = t["target"] + "_after"
    
    if src_label not in label_to_index or tgt_label not in label_to_index:
        continue

    sources.append(label_to_index[src_label])
    targets.append(label_to_index[tgt_label])
    values.append(t["value"])
    link_colors.append(group_colors[t["source"]])  # flow color based on source group

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=label_names,
        color=node_colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors
    )
)])

st.plotly_chart(fig, use_container_width=True)