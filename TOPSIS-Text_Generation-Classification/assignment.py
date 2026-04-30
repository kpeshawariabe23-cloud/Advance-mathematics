import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    "Model": ["GPT-2", "GPT-3.5-turbo", "LLaMA-2-7B", "Mistral-7B", "Falcon-7B"],
    "BLEU Score":          [0.312, 0.478, 0.445, 0.461, 0.389],
    "ROUGE-L":             [0.401, 0.563, 0.531, 0.548, 0.462],
    "Perplexity":          [18.4,  12.1,  13.8,  12.9,  15.6],
    "Inference Time (ms)": [120,   350,   280,   240,   260],
    "Model Size (GB)":     [0.5,   175.0, 13.5,  14.5,  7.0]
}

df = pd.DataFrame(data)

weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])

impacts = ["+", "+", "-", "-", "-"]

print("=" * 65)
print("TOPSIS Analysis for Text Generation Models")
print("=" * 65)
print("\nInitial Data:")
print(df.to_string(index=False))
print("-" * 65)

matrix = df.iloc[:, 1:].values.astype(float)
norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

weighted_matrix = norm_matrix * weights

ideal_best  = []
ideal_worst = []

for i in range(len(weights)):
    if impacts[i] == "+":
        ideal_best.append(weighted_matrix[:, i].max())
        ideal_worst.append(weighted_matrix[:, i].min())
    else:
        ideal_best.append(weighted_matrix[:, i].min())
        ideal_worst.append(weighted_matrix[:, i].max())

ideal_best  = np.array(ideal_best)
ideal_worst = np.array(ideal_worst)

dist_best  = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

topsis_score = dist_worst / (dist_best + dist_worst)

df["TOPSIS Score"] = topsis_score
df["Rank"] = df["TOPSIS Score"].rank(ascending=False).astype(int)

df_sorted = df.sort_values(by="Rank").reset_index(drop=True)

print("\nFinal Results (ranked):")
print(df_sorted.to_string(index=False))
print("=" * 65)

output_csv = "result.csv"
df_sorted.to_csv(output_csv, index=False)
print(f"\nResults saved to {output_csv}")

colors = ["#4CAF50", "#2196F3", "#FF9800", "#F44336", "#9C27B0"]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(df_sorted["Model"], df_sorted["TOPSIS Score"], color=colors,
              edgecolor="white", linewidth=0.8)

ax.set_xlabel("Text Generation Models", fontsize=12, labelpad=8)
ax.set_ylabel("TOPSIS Score", fontsize=12, labelpad=8)
ax.set_title("Comparison of Text Generation Models using TOPSIS", fontsize=14, fontweight="bold")
ax.set_ylim(0, 1.05)
ax.axhline(y=0.5, color="grey", linestyle="--", linewidth=0.8, alpha=0.7, label="Score = 0.5")
ax.legend(fontsize=9)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.012,
            f"{height:.3f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.tight_layout()
output_img = "topsis_graph.png"
plt.savefig(output_img, dpi=150)
print(f"Graph saved to {output_img}")
plt.show()
