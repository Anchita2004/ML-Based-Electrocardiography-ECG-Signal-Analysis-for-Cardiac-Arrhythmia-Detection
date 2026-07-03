import csv

signal_file = "100 Signal.csv"
annotation_file = "100 Annotation.csv"
output_file = "Segmented_Beats.csv"

fs = 360
pre_sec = 0.2
post_sec = 0.6

pre_samples = int(pre_sec * fs)
post_samples = int(post_sec * fs)
segment_len = pre_samples + post_samples

beats = ['N', 'A', 'V', '/', 'f', 'F', 'j', 'L', 'J', 'R', 'a', 'E', 'S', 'e']

signal = []
with open(signal_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        signal.append(float(row["MLII Analog"]))

ann_samples = []
ann_labels = []

with open(annotation_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ann_samples.append(int(row["Sample No."]))
        ann_labels.append(row["Symbol"])

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Start_Point", "End_Point", "Label"])

    for i in range(len(ann_samples)):

        sample = ann_samples[i]
        label = ann_labels[i]

        if label not in beats:
            continue

        start = sample - pre_samples
        end = sample + post_samples

        # Boundary check
        if start < 0 or end >= len(signal):
            continue

        # Extract segment
        segment = signal[start:end+1]

        row = [start, end, label] + segment + [label]
        writer.writerow(row)
