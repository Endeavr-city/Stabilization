import os

def delete_empty_files(label_path, image_path):
    # Iterate through all the .txt files in the label directory
    for file_name in os.listdir(label_path):
        # Check if the file is a .txt file
        if file_name.endswith('.txt'):
            file_path = os.path.join(label_path, file_name)
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                # Find corresponding image file
                image_file_name = file_name.replace('.txt', '.jpg')
                image_file_path = os.path.join(image_path, image_file_name)
                # Delete the .txt file
                os.remove(file_path)
                print(f"Deleted empty label file: {file_path}")
                # Check if the corresponding .jpg file exists and delete it
                if os.path.exists(image_file_path):
                    os.remove(image_file_path)
                    print(f"Deleted corresponding image file: {image_file_path}")

def process_directories(directories):
    for label_dir, image_dir in directories:
        delete_empty_files(label_dir, image_dir)

# List of tuples containing paths to the labels and images directories
directories = [
    ('./valid/labels/', './valid/images/'),
    ('./test/labels/', './test/images/'),
    ('./train/labels/', './train/images/')
]

# Call the function to process each directory pair
process_directories(directories)
