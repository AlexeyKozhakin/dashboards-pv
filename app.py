import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Заголовок
st.title("📊 Player Value Segment Evolution Dashboard")

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

