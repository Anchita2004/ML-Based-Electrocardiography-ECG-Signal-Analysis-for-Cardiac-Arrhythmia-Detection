import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# Source class folder (change to your class)
SOURCE_DIR = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\ECG_Plots\Balanced_beats\V"

# Output folder
OUTPUT_DIR = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Augmented_V"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ECG-safe augmentation
datagen = ImageDataGenerator(
    rotation_range=3,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.1,
    brightness_range=[0.95, 1.05],
    fill_mode='nearest'
)

# Number of augmented images per original image
AUG_PER_IMAGE = 5

for image_name in os.listdir(SOURCE_DIR):

    image_path = os.path.join(SOURCE_DIR, image_name)

    try:
        img = load_img(image_path, target_size=(224,224))
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        count = 0

        for batch in datagen.flow(
            x,
            batch_size=1,
            save_to_dir=OUTPUT_DIR,
            save_prefix=os.path.splitext(image_name)[0],
            save_format='png'
        ):
            count += 1

            if count >= AUG_PER_IMAGE:
                break

    except Exception as e:
        print(f"Error processing {image_name}: {e}")

print("Augmentation completed.")