import os
import csv
import pickle

# -------------------------------------------------
# Paths
# -------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

pickle_input = os.path.join(project_dir, "Processed-Signals", "balanced_data.pkl")
output_csv = os.path.join(project_dir, "Processed-Signals", "Segmented_Beats_Balanced.csv")

# -------------------------------------------------
# Load balanced dictionary from Part 1
# -------------------------------------------------
with open(pickle_input, "rb") as f:
    header, balanced_dict = pickle.load(f)

print("Loaded balanced dataset. Saving to CSV...")

# -------------------------------------------------
# Write Final Balanced CSV
# -------------------------------------------------
with open(output_csv, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for label in balanced_dict:
        for row in balanced_dict[label]:
            writer.writerow(row)

print(f"Balanced dataset saved to:\n{output_csv}")
