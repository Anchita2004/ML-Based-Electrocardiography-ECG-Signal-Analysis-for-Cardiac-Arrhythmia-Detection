import csv
import os
from collections import Counter

# ---- Paths ----
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

BALANCED_FILENAME = "Segmented_Beats_Balanced.csv"

balanced_csv = os.path.join(project_dir, "Processed-Signals", BALANCED_FILENAME)

# ---- Check if file exists ----
if not os.path.exists(balanced_csv):
    print("\nERROR: File not found:\n", balanced_csv)
    exit()

# ---- Count beats ----
label_counts = Counter()

with open(balanced_csv, "r") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        label = row[3]
        label_counts[label] += 1

print("\nBalanced dataset counts:\n")
for label, count in label_counts.items():
    status = "OK" if count == 5000 else f"NOT OK ({count})"
    print(f"{label}: {count} → {status}")
