import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# SETTINGS
# 

# Change these paths accordingly
#balanced_csv = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Processed-Signals\Segmented_Beats_Balanced.csv"
unbalanced_csv = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Processed-Signals\All_Patient_Segmented_Beats1.csv"

base_output_folder = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots"
df = pd.read_csv("All_Patient_Segmented_Beats1.csv")
print(df.shape)

fs = 360

# -------------------------------------------------
# FUNCTION TO GENERATE IMAGES
# -------------------------------------------------

def generate_images(csv_path, output_subfolder):

    df = pd.read_csv(csv_path)

    patient_ids = df.iloc[:, 0].to_numpy()   # Patient_ID
    labels = df.iloc[:, 3].to_numpy()        # Label
    ecg_data = df.iloc[:, 4:-1].to_numpy()   # ECG signals

    print(f"\nProcessing: {csv_path}")
    print("Unique Labels:", df.iloc[:, 3].unique())
    

    class_counters = {}

    for i in range(len(ecg_data)):

        signal = ecg_data[i]
        label = labels[i]
        patient_id = patient_ids[i]
        print(ecg_data.shape)
        print(ecg_data[0][:10])
        print(np.min(ecg_data), np.max(ecg_data))

        # Replace "/" safely
        if label == "/":
            label = "Paced"

        class_folder = os.path.join(output_subfolder, label)
        os.makedirs(class_folder, exist_ok=True)

        if label not in class_counters:
            class_counters[label] = 1
        else:
            class_counters[label] += 1

        time = np.arange(len(signal)) / fs

        fig = plt.figure(figsize=(2.24, 2.24), dpi=100)
        plt.plot(time, signal, linewidth=1)
        plt.axis("off")
        plt.tight_layout(pad=0)

        filename = f"{patient_id}_{label}{class_counters[label]}.png"
        save_path = os.path.join(class_folder, filename)

        plt.savefig(save_path, dpi=100)
        plt.close(fig)

    print(f"Images saved in {output_subfolder}")

# -------------------------------------------------
# CREATE MAIN FOLDERS
# -------------------------------------------------

#balanced_folder = os.path.join(base_output_folder, "balanced_beats")
unbalanced_folder = os.path.join(base_output_folder, "unbalanced_beats")

#os.makedirs(balanced_folder, exist_ok=True)
os.makedirs(unbalanced_folder, exist_ok=True)

# -------------------------------------------------
# GENERATE IMAGES
# -------------------------------------------------

generate_images(unbalanced_csv, unbalanced_folder)
#generate_images(balanced_csv, balanced_folder)

print("\nAll images generated successfully.")
