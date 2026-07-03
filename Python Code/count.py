import pandas as pd
import os

CSV_FILE = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Segmented_Signals\Segmented_Beats.csv"

# ------------------------------
# STEP 1: Read CSV properly
# ------------------------------

df = pd.read_csv(CSV_FILE, header=None)

print("Original Shape (including broken header row):", df.shape)

# Remove first row (broken header)
df = df.iloc[1:].reset_index(drop=True)

print("Shape after removing first row:", df.shape)

# ------------------------------
# STEP 2: Fix column names
# ------------------------------

metadata_columns = ["Patient_ID", "Start_Point", "End_Point", "Label", "Lead_Name"]

total_columns = df.shape[1]
signal_columns = [f"Signal_{i}" for i in range(total_columns - 5)]

df.columns = metadata_columns + signal_columns

print("Total Columns:", total_columns)
print("Total Signal Columns:", len(signal_columns))

# ------------------------------
# STEP 3: Check label information
# ------------------------------

print("\nUnique Labels in CSV:")
unique_labels = df["Label"].astype(str).str.strip().unique()
print(unique_labels)

print("\nTotal Unique Labels:", len(unique_labels))

print("\nLabel Distribution:")
print(df["Label"].astype(str).str.strip().value_counts())

# ------------------------------
# STEP 4: Check valid signals per label
# ------------------------------

valid_signal_count = {}

for index, row in df.iterrows():

    label = str(row["Label"]).strip()

    if label == "" or label.lower() == "nan":
        continue

    signal = pd.to_numeric(row[signal_columns], errors='coerce').dropna().values

    if len(signal) < 20:
        continue

    if label not in valid_signal_count:
        valid_signal_count[label] = 0

    valid_signal_count[label] += 1

print("\nValid Signals Per Label (will generate images):")
print(valid_signal_count)

print("\nLabels that will NOT generate images:")
missing_labels = set(unique_labels) - set(valid_signal_count.keys())
print(missing_labels)

print("\nTotal Images That Would Be Created:", sum(valid_signal_count.values()))