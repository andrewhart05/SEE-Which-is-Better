import tkinter as tk
from itertools import combinations
from PIL import Image, ImageTk
import csv
import os

def get_image_paths(folder_path):
    supported_formats = ['.jpg', '.jpeg', '.png']
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.splitext(f)[1].lower() in supported_formats and not f.endswith("GT.jpg") and not f.endswith("GT.jpeg") and not f.endswith("GT.png")]

def find_ground_truth_image(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith("GT.jpg") or file.endswith("GT.jpeg") or file.endswith("GT.png"):
            return os.path.join(folder_path, file)
    return None

def load_images(image_paths, size=(300, 300)):
    images = []
    for path in image_paths:
        image = Image.open(path)
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        images.append((photo, path))
    return images


def on_image_click(event, chosen_image, other_image):
    global choice_matrix, pair_index
    choice_matrix[chosen_image][other_image] = 1
    next_pair()


def next_pair():
    global pair_index, image_pairs, left_image_label, right_image_label
    pair_index += 1
    if pair_index >= len(image_pairs):
        var.set(1)
    else:
        left_photo, left_path = image_pairs[pair_index][0]
        right_photo, right_path = image_pairs[pair_index][1]
        left_image_label.config(image=left_photo)
        right_image_label.config(image=right_photo)
        left_image_label.bind("<Button-1>", lambda e: on_image_click(e, left_path, right_path))
        right_image_label.bind("<Button-1>", lambda e: on_image_click(e, right_path, left_path))


def save_matrix_to_csv(choice_matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image'] + list(choice_matrix.keys()))
        for row_image in choice_matrix:
            row = [row_image] + [choice_matrix[row_image].get(col_image, 0) for col_image in choice_matrix]
            writer.writerow(row)


def set_ground_image(ground_image_path):
    ground_image = Image.open(ground_image_path)
    ground_image = ground_image.resize(image_size)
    ground_photo = ImageTk.PhotoImage(ground_image)
    ground_image_label.config(image=ground_photo)
    ground_image_label.image = ground_photo  # Keep a reference


def process_folder(folder_path):
    global pair_index, image_pairs, choice_matrix

    ground_image_path = find_ground_truth_image(folder_path)
    if ground_image_path:
        set_ground_image(ground_image_path)
    else:
        print(f"No ground truth image found in {folder_path}. Skipping folder.")
        return

    image_paths = get_image_paths(folder_path)
    if len(image_paths) < 2:
        print(f"Not enough images in {folder_path}. Skipping.")
        return

    images = load_images(image_paths, size=image_size)
    image_pairs = list(combinations(images, 2))
    choice_matrix = {path: {other_path: 0 for other_path in image_paths if other_path != path} for path in image_paths}

    pair_index = -1
    next_pair()

    root.wait_variable(var)

    folder_name = os.path.basename(folder_path)
    csv_filename = f'{folder_name}_choices_matrix.csv'
    save_matrix_to_csv(choice_matrix, csv_filename)


# Initialize Tkinter
root = tk.Tk()
root.title("Which Is Better?")

question_label = tk.Label(root, text="Which Is Better?", font=("Times New Roman", 40, "bold"))
question_label.pack()

main_folder = 'images'
subfolders = [os.path.join(main_folder, f) for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

image_size = (300, 300)

ground_image_label = tk.Label(root)
ground_image_label.pack()

left_image_label = tk.Label(root, image=None)
left_image_label.pack(side="left")
right_image_label = tk.Label(root, image=None)
right_image_label.pack(side="right")

var = tk.IntVar()

for folder in subfolders:
    process_folder(folder)

root.mainloop()
