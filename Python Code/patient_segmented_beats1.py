import os
import csv
input_folder = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Extracted Signals"
output_folder = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Segmented_Signals"

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, "Segmented_Beats.csv")
fs = 360
pre_samples = int(0.2 * fs)
post_samples = int(0.6 * fs)

valid_beats = {'N','A','V','/','f','F','j','L','J','R','a','E','S','e'}
priority_leads = ["MLII Analog", "V1 Analog", "V5 Analog"]

with open(output_file, "w", newline="") as out_f:
    writer = csv.writer(out_f)

    # Header in requested order
    writer.writerow(["Patient_ID", "Start_Point", "End_Point", "Label", "Lead_Name"])

    for file in os.listdir(input_folder):
        if not file.endswith("Signal.csv"):
            continue

        patient_id = file.split()[0]
        signal_path = os.path.join(input_folder, f"{patient_id} Signal.csv")
        ann_path = os.path.join(input_folder, f"{patient_id} Annotation.csv")

        if not os.path.exists(ann_path):
            continue

        print(f"Processing {patient_id}...")

        # ---- Read Signal ----
        with open(signal_path) as f:
            reader = csv.reader(f)
            header = [h.strip() for h in next(reader)]

            lead = next((l for l in priority_leads if l in header), None)
            if not lead:
                lead = next((h for h in header if "Analog" in h), None)
            if not lead:
                continue

            col_idx = header.index(lead)
            signal = [float(r[col_idx]) for r in reader if len(r) > col_idx and r[col_idx] != ""]

        # ---- Read Annotations ----
        with open(ann_path) as f:
            reader = csv.DictReader(f)
            annotations = [(int(r["Sample No."]), r["Symbol"]) for r in reader]

        # ---- Extract Beats ----
        for sample, label in annotations:
            if label not in valid_beats:
                continue

            start = sample - pre_samples
            end = sample + post_samples

            if start < 0 or end >= len(signal):
                continue

            segment = signal[start:end+1]

            # Correct column order
            writer.writerow([patient_id, start, end, label, lead] + segment)

print("\nFinished. File saved to:", output_file)