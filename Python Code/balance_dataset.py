import os
import csv
import random
import pickle
from collections import defaultdict

# -------------------------------------------------
# Paths
# -------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

input_csv = os.path.join(project_dir, "Processed-Signals", "All_Patient_Segmented_Beats2.csv")
pickle_output = os.path.join(project_dir, "Processed-Signals", "balanced_data.pkl")

# -------------------------------------------------
# PARAMETERS (AS PER SIR)
# -------------------------------------------------
MAX_ALLOWED_LENGTH = 720
FINAL_LENGTH = 780
target_count = 5000

# -------------------------------------------------
# LOAD INPUT FILE
# -------------------------------------------------
segmented_beats_all_records_same_length = defaultdict(list)

with open(input_csv, "r") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        label = row[3]

        # ECG signal starts from index 4
        ecg_signal = row[4:]

        # -------------------------------------------------
        # STEP 1: KEEP ONLY BEATS WITH LENGTH ≤ 720
        # -------------------------------------------------
        if len(ecg_signal) <= MAX_ALLOWED_LENGTH:

            # -------------------------------------------------
            # STEP 2: EXTEND BEAT TO EXACTLY 780 POINTS
            # (Zero padding at the end)
            # -------------------------------------------------
            padded_signal = ecg_signal + ['0.0'] * (FINAL_LENGTH - len(ecg_signal))

            new_row = row[:4] + padded_signal
            segmented_beats_all_records_same_length[label].append(new_row)

# -------------------------------------------------
# DATASET BALANCING (SIR'S LOGIC)
# -------------------------------------------------
segmented_beats_all_records_same_length_balanced = {}

def random_augmentation(original_dataset, dataset_for_random_choice, required, full_dataset):
    augmented_dataset = list(original_dataset)

    for _ in range(required):
        if len(dataset_for_random_choice) == 0:
            dataset_for_random_choice.extend(full_dataset)

        indexed_list = list(enumerate(dataset_for_random_choice))
        selected_index, selected_beat = random.choice(indexed_list)

        dataset_for_random_choice.pop(selected_index)
        augmented_dataset.append(selected_beat)

    return augmented_dataset

# -------------------------------------------------
# APPLY BALANCING
# -------------------------------------------------
for class_label, class_beats in segmented_beats_all_records_same_length.items():

    current_count = len(class_beats)

    if current_count > target_count:
        # Downsampling
        dataset_copy = list(class_beats)
        balanced = random_augmentation([], dataset_copy, target_count, class_beats)
        segmented_beats_all_records_same_length_balanced[class_label] = balanced

    elif current_count < target_count:
        # Upsampling
        augmented = list(class_beats)
        dataset_copy = list(class_beats)
        current_count = len(augmented)

        while current_count != target_count:
            if (target_count - current_count) >= current_count:
                augmented.extend(class_beats)
            else:
                required = target_count - current_count
                augmented.extend(
                    random_augmentation([], dataset_copy, required, class_beats)
                )
            current_count = len(augmented)

        segmented_beats_all_records_same_length_balanced[class_label] = augmented

    else:
        segmented_beats_all_records_same_length_balanced[class_label] = class_beats

# -------------------------------------------------
# SAVE BALANCED DATASET (FOR CNN)
# -------------------------------------------------
with open(pickle_output, "wb") as f:
    pickle.dump((header[:4] + [f"ECG_{i+1}" for i in range(FINAL_LENGTH)],
                 segmented_beats_all_records_same_length_balanced), f)

print("✔ Balanced dataset saved with:")
print("  - Only beats of length ≤ 720")
print("  - All beats padded to 780 points")
print("  - Exactly 5000 beats per class")