from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

files = [
    "GA_RouletWheelHB.xlsx",
    "GA_RankSelectionHB.xlsx",
    "GA_TournamentSelectionHB.xlsx",
    "GA_SS_RouletWheelHB.xlsx",
    "GA_SS_RankSelectionHB.xlsx",
    "GA_SS_TournamentSelectionHB.xlsx"
]
labels = [
    "N Roulette",
    "N Rank",
    "N Tournament",
    "St.S Roulette",
    "St.S Rank",
    "St.S Tournament"
]

fitness_data = []
time_data = []

for file in files:
    df = pd.read_excel(file)

    fitness_data.append(df["Fitness"].dropna())
    time_data.append(df["Time (s)"].dropna())

fig, ax1 = plt.subplots(figsize=(12, 7))
#plt.figure(figsize=(12, 7))
positions = np.arange(1, len(files) +1)

bp1 = ax1.boxplot(
    fitness_data,
    positions=positions - 0.15,
    widths=0.25,
    patch_artist=True,
    showmeans=True
)


ax2 = ax1.twinx()

bp2 = ax2.boxplot(
    time_data,
    positions=positions + 0.15,
    widths=0.25,
    patch_artist=True,
    showmeans=True
)


for box in bp1["boxes"]:
    box.set_facecolor("skyblue")

for box in bp2["boxes"]:
    box.set_facecolor("lightcoral")

# Axes
ax1.set_xlabel("GA configuration")
ax1.set_ylabel("Fitness")
ax2.set_ylabel("Execution time (s)")

ax1.set_xticks(positions)
ax1.set_xticklabels(labels, rotation=20)

ax1.set_title("Fitness and Execution Time Comparison Himmelblau")

ax1.grid(axis="y", alpha=0.3)

ax1.set_ylim(-10, 0.1)
ax2.set_ylim(40, 0.05)
legend_elements = [
    Patch(facecolor="skyblue", label="Fitness"),
    Patch(facecolor="lightcoral", label="Execution time")
]

ax1.legend(handles=legend_elements, loc="upper right")

plt.tight_layout()
plt.show()