import tkinter as tk
from itertools import combinations
from PIL import Image, ImageTk
import csv
import os

# Get paths of all images in a folder besides original images
def get_image_paths(folder_path):
    supported_formats = ['.jpg', '.jpeg', '.png']
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.splitext(f)[1].lower() in supported_formats and not f.endswith("og.jpg") and not f.endswith("og.jpeg") and not f.endswith("og.png")]

# Find the original image in a folder
def find_original_image(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith("og.jpg") or file.endswith("og.jpeg") or file.endswith("og.png"):
            return os.path.join(folder_path, file)
    return None

# Function to load and resize images from a list of paths
def load_images(image_paths, size=(300, 300)):
    images = []
    for path in image_paths:
        image = Image.open(path)
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        images.append((photo, path))
    return images

# Event handler for image clicks
def on_image_click(event, chosen_image, other_image):
    global choice_matrix, pair_index
    choice_matrix[chosen_image][other_image] = 1
    next_pair()

# Display the next pair of images or finish the process
def next_pair():
    global pair_index, image_pairs, left_image_label, right_image_label, is_last_folder
    pair_index += 1
    if pair_index >= len(image_pairs):
        var.set(1)  
        if is_last_folder:
            root.destroy()  
    else:
        # Display the next pair of images
        left_photo, left_path = image_pairs[pair_index][0]
        right_photo, right_path = image_pairs[pair_index][1]
        left_image_label.config(image=left_photo)
        right_image_label.config(image=right_photo)
        # Bind click events to the images
        left_image_label.bind("<Button-1>", lambda e: on_image_click(e, left_path, right_path))
        right_image_label.bind("<Button-1>", lambda e: on_image_click(e, right_path, left_path))

# Save the choice matrix to a CSV file
def save_matrix_to_csv(choice_matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image'] + list(choice_matrix.keys()))
        for row_image in choice_matrix:
            row = [row_image] + [choice_matrix[row_image].get(col_image, 0) for col_image in choice_matrix]
            writer.writerow(row)

# Set the original image at the top of the window
def set_ground_image(ground_image_path):
    ground_image = Image.open(ground_image_path)
    ground_image = ground_image.resize(image_size)
    ground_photo = ImageTk.PhotoImage(ground_image)
    ground_image_label.config(image=ground_photo)
    ground_image_label.image = ground_photo  # Reference to avoid garbage collection

# Process each image folder
def process_folder(folder_path, is_last):
    global pair_index, image_pairs, choice_matrix, is_last_folder
    is_last_folder = is_last

    # Set the original image for the current folder
    ground_image_path = find_original_image(folder_path)
    if ground_image_path:
        set_ground_image(ground_image_path)

    # Load and prepare image pairs for comparison
    image_paths = get_image_paths(folder_path)
    images = load_images(image_paths, size=image_size)
    image_pairs = list(combinations(images, 2))
    choice_matrix = {path: {other_path: 0 for other_path in image_paths if other_path != path} for path in image_paths}

    pair_index = -1
    next_pair()

    # Wait until all pairs in the current folder are processed
    root.wait_variable(var)

    # Save the choice matrix to a CSV file
    folder_name = os.path.basename(folder_path)
    csv_filename = f'{folder_name}_choices_matrix.csv'
    save_matrix_to_csv(choice_matrix, csv_filename)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Which Is Better?")

question_label = tk.Label(root, text="Which Is Better?", font=("Times New Roman", 40, "bold"))
question_label.pack()

main_folder = 'images'
subfolders = [os.path.join(main_folder, f) for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

image_size = (300, 300)

# Labels for displaying images
ground_image_label = tk.Label(root)
ground_image_label.pack()
left_image_label = tk.Label(root, image=None)
left_image_label.pack(side="left")
right_image_label = tk.Label(root, image=None)
right_image_label.pack(side="right")

var = tk.IntVar()

# Process each subfolder
is_last_folder = False
for index, folder in enumerate(subfolders):
    is_last = (index == len(subfolders) - 1)
    process_folder(folder, is_last)

root.mainloop()
