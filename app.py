import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import random


# Заголовок
st.title("📊 Player Value Groups Evolution")

# Автоматическая загрузка файла
file_path = "player_value_simulation.csv"

if not os.path.exists(file_path):
    st.error(f"Файл `{file_path}` не найден в директории проекта.")
else:
    data = pd.read_csv(file_path)

    # Убедимся, что колонка month в формате datetime
    data["month"] = pd.to_datetime(data["month"]).dt.to_period("M").astype(str)

    # 🎯 Классификация по сегментам
    def classify_player_value(pv):
        if pv < 150:
            return "low"
        elif pv < 1000:
            return "medium"
        elif pv < 2500:
            return "high"
        elif pv < 10000:
            return "pvip"
        elif pv < 15000:
            return "vip"
        else:
            return "svip"

    data["segment"] = data["player_value"].apply(classify_player_value)

    # 📊 Группируем по месяцу и сегменту
    grouped = data.groupby(["month", "segment"])["user_id"].count().unstack(fill_value=0).reset_index()
    grouped = grouped.set_index("month")

    # Упорядочим сегменты и зададим цвета
    segment_order = ["low", "medium", "high", "pvip", "vip", "svip"]
    colors = {
        "low": "#D3D3D3",
        "medium": "#87CEFA",
        "high": "#6495ED",
        "pvip": "#FFD700",
        "vip": "#FF8C00",
        "svip": "#FF4500"
    }

    # Убедимся, что все сегменты есть в колонках
    for seg in segment_order:
        if seg not in grouped.columns:
            grouped[seg] = 0
    grouped = grouped[segment_order]

    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    # Общий стиль шрифта для жирных подписей
    bold_font = {'fontsize': 15, 'fontweight': 'bold'}

    n_segments = len(segment_order)
    fig, axes = plt.subplots(n_segments, 1, figsize=(14, 3 * n_segments), sharex=True)

    for i, segment in enumerate(segment_order):
        ax = axes[i]
        grouped[segment].plot(kind="area", color=colors[segment], ax=ax)
        ax.set_title(f"Segment: {segment}", fontsize=16, fontweight='bold', loc='left')
        ax.set_ylabel("Players", fontsize=12, fontweight='bold')
        
        # Настройка жирных цифр на осях
        for label in ax.get_yticklabels():
            label.set_fontsize(11)
            label.set_fontweight('bold')
        for label in ax.get_xticklabels():
            label.set_fontsize(11)
            label.set_fontweight('bold')
        
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Month", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ==================== Segments Flow

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Заголовок
st.title("🎯 Player Retention-Churn-Reactivation Flow")

# Порядок сегментов и статусов
segments = ["Low", "Medium", "High", "PVIP", "VIP", "SVIP"]
statuses = ["Churned", "Retained", "Reactivated"]

# 🎲 Генерация искусственных данных
np.random.seed(42)
data = []
for segment in segments:
    churned = np.random.randint(100, 300)
    retained = np.random.randint(200, 500)
    reactivated = np.random.randint(50, 150)
    data.append([segment, "Churned", churned])
    data.append([segment, "Reactivated", reactivated])
    data.append([segment, "Retained", retained])

df = pd.DataFrame(data, columns=["segment", "status", "count"])

# Метки и индексация
all_labels = segments + statuses
label_to_index = {label: i for i, label in enumerate(all_labels)}

# Источники и назначения
df["source"] = df["segment"].map(label_to_index)
df["target"] = df["status"].map(label_to_index)

# 🎨 Цвета по статусу
status_colors = {
    "Churned": "rgba(255, 99, 71, 0.6)",       # Красный
    "Reactivated": "rgba(255, 215, 0, 0.6)",   # Жёлтый
    "Retained": "rgba(34, 139, 34, 0.6)"       # Зелёный
}
df["color"] = df["status"].map(status_colors)
# Построение диаграммы
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
        color="lightblue"
    ),
    link=dict(
        source=df["source"],
        target=df["target"],
        value=df["count"],
        color=df["color"]
    )
)])

st.plotly_chart(fig, use_container_width=True)



# ============= TRANSITIONS =================


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