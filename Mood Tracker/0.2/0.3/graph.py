import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Load data from JSON file
with open("smartwatchrandom_data.json", "r") as f:
    data = json.load(f)

# Extract data for each metric
steps = data["Steps"]
calories = data["Calories"]
heart_rate = data["Heart Rate"]
fuck = data["FUCK"]

# Create x array with labels for each day
x = np.array(["Day 1", "Day 2", "Day 3", "Day 4"])

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot steps walked
axs[0, 0].plot(x, steps, marker='o')
axs[0, 0].grid(axis='y', color='green', linestyle='--', linewidth=0.5)
axs[0, 0].set_xlabel("Days")
axs[0, 0].set_ylabel("Steps Walked")

# Plot calories burned
axs[0, 1].plot(x, calories, marker='o')
axs[0, 1].grid(axis='y', color='green', linestyle='--', linewidth=0.5)
axs[0, 1].set_xlabel("Days")
axs[0, 1].set_ylabel("Calories Burned")

# Plot heart rate
axs[1, 0].plot(x, heart_rate, marker='o')
axs[1, 0].grid(axis='y', color='green', linestyle='--', linewidth=0.5)
axs[1, 0].set_xlabel("Days")
axs[1, 0].set_ylabel("Heart Rate")

# Plot the "FUCK" metric
axs[1, 1].plot(x, fuck, marker='o')
axs[1, 1].grid(axis='y', color='green', linestyle='--', linewidth=0.5)
axs[1, 1].set_xlabel("Days")
axs[1, 1].set_ylabel("FUCK")

# Set suptitle
fig.suptitle("Smartwatch Metrics")

# Display the plot
plt.show()

# Save the plot to a file
plt.savefig(sys.stdout.buffer)
sys.stdout.flush()
