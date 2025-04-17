import pandas as pd
import numpy as np

# 📌 Параметры
n_users = 1000
n_months = 12
mean_log = 4.05  # Среднее для log-нормального распределения
sigma_log = 1.96  # Дисперсия для log-нормального распределения

# 📅 Генерируем месяцы
months = pd.date_range(start="2024-01-01", periods=n_months, freq='MS').strftime('%Y-%m')

# 👥 Генерируем user_id
user_ids = [f"user_{i+1}" for i in range(n_users)]

# 🧪 Генерация данных
rows = []
for user_id in user_ids:
    for month in months:
        value = np.random.lognormal(mean=mean_log, sigma=sigma_log)  # ~100 до ~100000
        rows.append([user_id, month, round(value, 2)])

# 📊 В DataFrame
df = pd.DataFrame(rows, columns=["user_id", "month", "player_value"])

# 💾 Сохраняем в CSV
df.to_csv("player_value_simulation.csv", index=False)

print("✅ CSV файл создан: player_value_simulation.csv")