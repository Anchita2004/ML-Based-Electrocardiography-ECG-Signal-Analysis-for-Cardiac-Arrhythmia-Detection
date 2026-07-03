import csv

# --- File names ---
signal_file = '100 Signal.csv'
annotation_file = '100 Annotation.csv'
output_file = 'Readable_ECG_Segments_With_Types.csv'

# --- Beat symbols as per your sir's instruction ---
consider = ['N', 'A', 'V', '/', 'f', 'F', 'j', 'L', 'J', 'R', 'a', 'E', 'S', 'e']
ignore = ['~', '+', '"']
discard = ['|', 'Q', 'x', '[', '!', ']']

# --- Read signal data ---
signal_data = []
with open(signal_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        signal_data.append({
            'Sampling Number': int(row['Sampling Number']),
            'MLII Analog': float(row['MLII Analog'])
        })

# --- Read annotation data ---
anno_data = []
with open(annotation_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        symbol = row['Symbol']
        if symbol not in ignore and symbol not in discard:  # only keep valid ones
            anno_data.append({
                'Sample No.': int(row['Sample No.']),
                'Symbol': symbol
            })

# --- Create output file ---
with open(output_file, 'w', newline='') as f_out:
    writer = csv.writer(f_out)

    # Write header
    writer.writerow(['Beat Pair', 'Start Sample', 'End Sample', 'Beat Type', 'ECG Values...', 'Symbol'])

    # --- Main Loop ---
    for i in range(len(anno_data) - 1):
        beat1 = anno_data[i]
        beat2 = anno_data[i + 1]

        # Only consider valid symbols
        if beat1['Symbol'] in consider and beat2['Symbol'] in consider:
            start = beat1['Sample No.']
            end = beat2['Sample No.']

            # Extract ECG samples between start and end
            segment = [s['MLII Analog'] for s in signal_data if start <= s['Sampling Number'] < end]

            # Create metadata
            beat_pair = f"{beat1['Symbol']}_to_{beat2['Symbol']}"
            beat_type = 'Normal' if (beat1['Symbol'] == 'N' and beat2['Symbol'] == 'N') else 'Abnormal'

            # Append beat2 symbol at end
            segment.append(beat2['Symbol'])

            # Combine everything into one row
            row = [beat_pair, start, end, beat_type] + segment

            # Write to CSV
            writer.writerow(row)

print("ECG segments written successfully to:", output_file)
