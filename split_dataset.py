import os
import shutil
import random

# Path to your original raw images
raw_dir = "raw-img"  # change if different
output_dir = "animals-10"  # new dataset structure

# Train/Validation split ratio
train_ratio = 0.8

# Create train/val folders
train_dir = os.path.join(output_dir, "train")
val_dir = os.path.join(output_dir, "val")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Loop through each class folder in raw-img
for class_name in os.listdir(raw_dir):
    class_path = os.path.join(raw_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    # Create class subfolders in train and val
    train_class_dir = os.path.join(train_dir, class_name)
    val_class_dir = os.path.join(val_dir, class_name)
    os.makedirs(train_class_dir, exist_ok=True)
    os.makedirs(val_class_dir, exist_ok=True)

    # List all images in class folder
    images = os.listdir(class_path)
    random.shuffle(images)

    # Split images
    train_count = int(len(images) * train_ratio)
    train_images = images[:train_count]
    val_images = images[train_count:]

    # Copy images to train folder
    for img in train_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(train_class_dir, img))

    # Copy images to val folder
    for img in val_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(val_class_dir, img))

print("Dataset split complete!")
print(f"Train folder: {train_dir}")
print(f"Validation folder: {val_dir}")
