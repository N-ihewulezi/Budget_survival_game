
import pandas as pd
import numpy as np

np.random.seed(42)
days = list(range(1, 31))
categories = {'Food': 800, 'Transport': 500, 'Utilities': 300, 'Airtime/Data': 200, 'Emergency': 0}
data = []

for day in days:
    inflation = np.random.uniform(0.01, 0.05)
    row = {"Day": day, "InflationRate": round(inflation * 100, 2)}
    for item, base in categories.items():
        if item == "Emergency":
            row[item] = np.random.choice([0, 1000, 2000], p=[0.8, 0.1, 0.1])
        else:
            row[item] = round(base * (1 + inflation)**day, -1)
    data.append(row)

df = pd.DataFrame(data)
df.to_csv("price_simulation.csv", index=False)
print("price_simulation.csv created.")
