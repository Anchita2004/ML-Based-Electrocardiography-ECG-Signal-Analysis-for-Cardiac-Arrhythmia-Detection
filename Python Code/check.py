import os

BALANCED_DIR = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Balanced_beats"

target_count = 5000

print("\nChecking folder counts...\n")

for folder in os.listdir(BALANCED_DIR):

    folder_path = os.path.join(BALANCED_DIR, folder)

    if os.path.isdir(folder_path):

        images = [f for f in os.listdir(folder_path) if f.endswith(".png")]

        count = len(images)

        if count == target_count:
            status = "OK"
        else:
            status = "ERROR"

        print(f"{folder} : {count} images  ---> {status}")

print("\nCheck completed.")