import matplotlib
matplotlib.use('Agg')

import os
import random
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# FILE PATHS
# ===============================

CSV_FILE = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Segmented_Signals\Segmented_Beats.csv"

OUTPUT_DIR = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Balanced_beats"

os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_COUNT = 5000

# ===============================
# READ CSV
# ===============================

df = pd.read_csv(CSV_FILE, header=None, low_memory=False)

print("Original Shape:", df.shape)

df = df.iloc[1:].reset_index(drop=True)

print("After removing first row:", df.shape)

# ===============================
# FILTER ONLY REQUIRED LABELS
# ===============================

selected_labels = ['A', 'V', 'L', 'R', '/', 'N']

df = df[df.iloc[:,3].isin(selected_labels)]

# ===============================
# GROUP DATA BY CLASS
# ===============================

grouped = {}

for label in selected_labels:
    grouped[label] = df[df.iloc[:,3] == label].values.tolist()

# ===============================
# BALANCING FUNCTION
# ===============================

def balance_dataset(dataset, target_count):

    current_dataset = dataset.copy()
    current_count = len(current_dataset)

    # ================= UPSAMPLING =================
    if current_count < target_count:

        dataset_for_random_choice = current_dataset.copy()
        augmented_dataset = current_dataset.copy()

        current_count = len(augmented_dataset)

        while current_count != target_count:

            if (target_count - current_count) >= len(current_dataset):

                augmented_dataset.extend(current_dataset)

            else:

                needed = target_count - current_count

                temp_list = dataset_for_random_choice.copy()

                for _ in range(needed):

                    choice = random.choice(temp_list)

                    temp_list.remove(choice)

                    augmented_dataset.append(choice)

            current_count = len(augmented_dataset)

        return augmented_dataset[:target_count]

    # ================= DOWNSAMPLING =================

    elif current_count > target_count:

        dataset_copy = dataset.copy()

        chosen_dataset = []

        for _ in range(target_count):

            choice = random.choice(dataset_copy)

            dataset_copy.remove(choice)

            chosen_dataset.append(choice)

        return chosen_dataset

    else:

        return dataset


# ===============================
# BALANCE ALL CLASSES
# ===============================

balanced_data = {}

for label in selected_labels:

    print(f"\nProcessing class {label}")

    dataset = grouped[label]

    balanced_dataset = balance_dataset(dataset, TARGET_COUNT)

    balanced_data[label] = balanced_dataset

    print("Final count:", len(balanced_dataset))


# ===============================
# IMAGE GENERATION
# ===============================

image_count = 0

for label in selected_labels:

    folder_name = "slash" if label == "/" else label

    label_folder = os.path.join(OUTPUT_DIR, folder_name)

    os.makedirs(label_folder, exist_ok=True)

    class_data = balanced_data[label]

    counter = 1

    for row in class_data:

        patient_id = str(row[0]).strip()

        signal = pd.to_numeric(pd.Series(row[5:]), errors='coerce')
        signal = signal.dropna().values

        if len(signal) == 0:
            continue

        filename = f"{patient_id}_{folder_name}_{counter}.png"

        save_path = os.path.join(label_folder, filename)

        plt.figure(figsize=(2.24, 2.24), dpi=100)
        plt.plot(signal)
        plt.axis('off')
        plt.tight_layout(pad=0)

        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)

        plt.close()

        counter += 1
        image_count += 1


# ===============================
# SUMMARY
# ===============================

print("\nTotal images generated:", image_count)

print("\nBalanced folders created:")

for folder in os.listdir(OUTPUT_DIR):
    print(folder)