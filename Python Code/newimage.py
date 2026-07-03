import matplotlib
matplotlib.use('Agg')

import os
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# CSV FILE PATH
# ================================
CSV_FILE = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Segmented_Signals\Segmented_Beats.csv"

# ================================
# OUTPUT DIRECTORY
# ================================
OUTPUT_DIR = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Unbalanced_beats"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# READ CSV
# ================================
df = pd.read_csv(CSV_FILE, header=None, low_memory=False)

print("Original Shape:", df.shape)

# Remove broken header row
df = df.iloc[1:].reset_index(drop=True)

print("After removing first row:", df.shape)

# ================================
# COUNTERS
# ================================
class_counter = {}
image_count = 0

# ================================
# LOOP THROUGH ROWS
# ================================
for index, row in df.iterrows():

    # Metadata columns
    patient_id = str(row.iloc[0]).strip()
    label = str(row.iloc[3]).strip()

    if not label or label == 'nan':
        continue

    # Fix "/" label
    if label == "/":
        label = "slash"

    # ECG signal starts from column 5 onward
    signal = pd.to_numeric(row.iloc[5:], errors='coerce').dropna().values

    if len(signal) == 0:
        continue

    # ================================
    # CREATE LABEL FOLDER
    # ================================
    label_folder = os.path.join(OUTPUT_DIR, label)
    os.makedirs(label_folder, exist_ok=True)

    # Initialize counter
    if label not in class_counter:
        class_counter[label] = 1

    # ================================
    # IMAGE NAME WITH PATIENT ID
    # ================================
    filename = f"{patient_id}_{label}_{class_counter[label]}.png"
    save_path = os.path.join(label_folder, filename)

    # ================================
    # PLOT ECG
    # ================================
    plt.figure(figsize=(2.24, 2.24), dpi=100)
    plt.plot(signal)
    plt.axis('off')
    plt.tight_layout(pad=0)

    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    class_counter[label] += 1
    image_count += 1

# ================================
# SUMMARY
# ================================
print("\nTotal images created:", image_count)
print("\nFolders created:")

for folder in os.listdir(OUTPUT_DIR):
    print(folder)