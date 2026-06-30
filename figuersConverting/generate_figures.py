import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
    }
)

kp = np.array([50, 100, 200, 1000])
manual = np.array([390, 780, 1560, 7800])
ai1 = np.array([1.0, 2.0, 4.0, 20.0])
ai6 = np.array([0.2, 0.4, 0.8, 4.0])

# Figure 5.1
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(kp))
w = 0.25
ax.bar(x - w, manual, w, label="Manual Method")
ax.bar(x, ai1, w, label="AI (1 Worker)")
ax.bar(x + w, ai6, w, label="AI (6 Workers)")
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(kp)
ax.set_xlabel("Number of KPIs Processed")
ax.set_ylabel("Time in Minutes (Log Scale)")
ax.set_title("Performance Time Comparison: Manual vs. AI Methods")
ax.legend()
fig.tight_layout()
fig.savefig("image7.svg")
plt.close(fig)

# Figure 5.2
fig, axs = plt.subplots(3, 1, figsize=(8, 12))
axs[0].plot(kp, manual, marker="o", label="Manual Method")
axs[0].plot(kp, ai1, marker="o", label="AI (1 Worker)")
axs[0].plot(kp, ai6, marker="o", label="AI (6 Workers)")
axs[0].set_yscale("log")
axs[0].set_title("Time vs. Number of KPIs (Log Scale)")
axs[0].set_ylabel("Time (minutes)")
axs[0].legend()

axs[1].bar(x - 0.15, manual / ai1, 0.3, label="AI Speedup (1 Worker)")
axs[1].bar(x + 0.15, manual / ai6, 0.3, label="AI Speedup (6 Workers)")
axs[1].set_xticks(x)
axs[1].set_xticklabels(kp)
axs[1].set_ylabel("Times Faster (×)")
axs[1].set_title("Speedup Factor Relative to Manual Method")
axs[1].legend()

axs[2].bar(x - 0.15, (1 - ai1 / manual) * 100, 0.3, label="Time Reduction % (1 Worker)")
axs[2].bar(
    x + 0.15, (1 - ai6 / manual) * 100, 0.3, label="Time Reduction % (6 Workers)"
)
axs[2].set_ylim(99.5, 100)
axs[2].set_title("Percentage Time Reduction vs. Manual Method")
axs[2].legend()

fig.tight_layout()
fig.savefig("image8.svg")
plt.close(fig)

# Figure 5.3
labels = [1, 2, 3, 4, 5]
counts = [0, 1, 1, 7, 11]
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(labels, counts)
ax.set_xlabel("Likert Response (1 = Strongly Disagree, 5 = Strongly Agree)")
ax.set_ylabel("Number of Responses")
ax.set_title("Survey: Interface Intuitiveness (N = 20)")
fig.tight_layout()
fig.savefig("image9.svg")
plt.close(fig)

# Enforce minimum readable font sizes (BAJ-compliant)

labels = ["Yes, significantly", "Slightly", "No change", "Unsure"]

counts = [46, 5, 5, 4]  # N = 60

colors = ["#4C72B0", "#DD8452", "#E6B800", "#55A868"]

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(labels, counts, color=colors)

ax.set_ylabel("Number of Responses")
ax.set_title("Perceived Potential of the Tool to Reduce KPI Reporting Errors (N = 60)")

# Add value labels on bars
for i, v in enumerate(counts):
    ax.text(i, v + 0.8, f"{v} ({v / 60:.1%})", ha="center", fontsize=9)

fig.tight_layout()
fig.savefig("image10.svg")
plt.close(fig)
