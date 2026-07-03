import os
import random
from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array
)

# Source folder containing original A images
SOURCE_FOLDER = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Balanced_beats\A"

# Folder where augmented images will be stored
OUTPUT_FOLDER = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Balanced_beats\Augmented_A"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Number of augmented images required
TARGET_AUGMENTED_IMAGES = 5000

# ECG-safe augmentations
datagen = ImageDataGenerator(
    rotation_range=3,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.10,
    brightness_range=[0.95, 1.05],
    fill_mode='nearest'
)

# Original image list
image_files = [
    f for f in os.listdir(SOURCE_FOLDER)
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
]

generated = 0

print(f"Generating {TARGET_AUGMENTED_IMAGES} augmented images...")

while generated < TARGET_AUGMENTED_IMAGES:

    image_name = random.choice(image_files)

    image_path = os.path.join(SOURCE_FOLDER, image_name)

    img = load_img(image_path, target_size=(224, 224))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    for _ in datagen.flow(
        x,
        batch_size=1,
        save_to_dir=OUTPUT_FOLDER,
        save_prefix=f"aug_{generated}",
        save_format='png'
    ):
        generated += 1

        if generated % 100 == 0:
            print(f"Generated {generated}/{TARGET_AUGMENTED_IMAGES}")

        break

print("\nAugmentation completed!")
print(f"Total images created in Augmented_A: {generated}")