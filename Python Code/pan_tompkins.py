import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks
import os

# -------------------------------------------------
# SETTINGS
# -------------------------------------------------
FS = 100                         # Sampling frequency
TOL_MS = 50                      # tolerance in ms
TOL = int((TOL_MS / 1000) * FS)  # tolerance in samples

# -------------------------------------------------
# BANDPASS FILTER FUNCTION
# -------------------------------------------------
def bandpass_filter(signal, fs):
    low = 5 / (fs / 2)
    high = 15 / (fs / 2)
    b, a = butter(1, [low, high], btype='band')
    return filtfilt(b, a, signal)

# -------------------------------------------------
# PATH SETTINGS
# -------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

signals_folder = os.path.join(project_dir, "Extracted Signals")
output_main_folder = os.path.join(project_dir, "PanTompkins_Output")
os.makedirs(output_main_folder, exist_ok=True)

# -------------------------------------------------
# PROCESS EACH SIGNAL
# -------------------------------------------------
for file in os.listdir(signals_folder):

    if file.endswith("Signal.csv"):

        record_id = file.split()[0]

        signal_path = os.path.join(signals_folder, f"{record_id} Signal.csv")
        annotation_path = os.path.join(signals_folder, f"{record_id} Annotation.csv")

        if not os.path.exists(annotation_path):
            continue

        print(f"\nProcessing Record {record_id}...")

        # Create output folder for this record
        record_output_folder = os.path.join(output_main_folder, record_id)
        os.makedirs(record_output_folder, exist_ok=True)

        # -------------------------------------------------
        # LOAD SIGNAL
        # -------------------------------------------------
        df_signal = pd.read_csv(signal_path)
        df_signal.columns = df_signal.columns.str.strip()

        # Priority logic: MLII first, else V5
        if "MLII Calculated" in df_signal.columns:
            ecg_column = "MLII Calculated"
        elif "V5 Calculated" in df_signal.columns:
            ecg_column = "V5 Calculated"
        else:
            print(f"No suitable ECG column found for record {record_id}")
            continue

        print(f"Using column: {ecg_column}")
        ecg = df_signal[ecg_column].to_numpy()

        # -------------------------------------------------
        # PAN-TOMPKINS
        # -------------------------------------------------
        filtered = bandpass_filter(ecg, FS)

        diff_signal = np.diff(filtered)
        diff_signal = np.append(diff_signal, 0)

        squared = diff_signal ** 2

        window_size = int(0.15 * FS)
        mwi = np.convolve(squared, np.ones(window_size)/window_size, mode='same')

        peaks, _ = find_peaks(
            mwi,
            distance=int(0.25 * FS),
            height=np.mean(mwi) + 0.5*np.std(mwi)
        )

        detected_r_peaks = peaks
        print("Detected R-peaks:", len(detected_r_peaks))

        # -------------------------------------------------
        # SAVE NEW ANNOTATION
        # -------------------------------------------------
        new_annotation_df = pd.DataFrame({
            "Sample No.": detected_r_peaks,
            "Symbol": ["R"] * len(detected_r_peaks)
        })

        new_annotation_path = os.path.join(
            record_output_folder,
            f"{record_id}_PanTompkins_Annotation.csv"
        )
        new_annotation_df.to_csv(new_annotation_path, index=False)

        # -------------------------------------------------
        # LOAD ORIGINAL ANNOTATION
        # -------------------------------------------------
        df_original = pd.read_csv(annotation_path)
        true_r_peaks = df_original["Sample No."].to_numpy()

        # -------------------------------------------------
        # COMPARISON
        # -------------------------------------------------
        comparison_results = []
        matched_true = set()

        for d in detected_r_peaks:
            matched = False
            for i, t in enumerate(true_r_peaks):
                if abs(d - t) <= TOL:
                    comparison_results.append([d, t, "TP"])
                    matched_true.add(i)
                    matched = True
                    break
            if not matched:
                comparison_results.append([d, "-", "FP"])

        for i, t in enumerate(true_r_peaks):
            if i not in matched_true:
                comparison_results.append(["-", t, "FN"])

        comparison_df = pd.DataFrame(
            comparison_results,
            columns=["Detected_Sample", "True_Sample", "Result"]
        )

        comparison_path = os.path.join(
            record_output_folder,
            f"{record_id}_Comparison.csv"
        )
        comparison_df.to_csv(comparison_path, index=False)

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------
        TP = sum(comparison_df["Result"] == "TP")
        FP = sum(comparison_df["Result"] == "FP")
        FN = sum(comparison_df["Result"] == "FN")

        sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0

        print("TP:", TP, "FP:", FP, "FN:", FN)
        print("Sensitivity:", round(sensitivity, 4))
        print("Precision:", round(precision, 4))

print("\nAll records processed successfully.")
