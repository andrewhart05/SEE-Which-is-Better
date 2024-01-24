import tkinter as tk
from itertools import combinations
from PIL import Image, ImageTk
import csv
import zipfile
import os

def get_image_paths(folder_path):
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in supported_formats]

def load_images(image_paths, size=(300, 300)):
    images = []
    for path in image_paths:
        image = Image.open(path)
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        images.append((photo, path))
    return images

def next_pair():
    global pair_index
    pair_index += 1
    if pair_index >= len(image_pairs):
        save_matrix_to_csv()
        root.quit()
    else:
        update_images()

def update_images():
    left_image_label.config(image=image_pairs[pair_index][0][0])
    right_image_label.config(image=image_pairs[pair_index][1][0])

def on_image_click(event, chosen_image, other_image):
    choice_matrix[chosen_image][other_image] = 1
    next_pair()

def save_matrix_to_csv():
    with open('image_choices_matrix.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image'] + image_paths)
        for row_image in image_paths:
            row = [row_image] + [choice_matrix[row_image].get(col_image, 0) for col_image in image_paths]
            writer.writerow(row)

root = tk.Tk()
root.title("Which Is Better?")

question_label = tk.Label(root, text="Which is Better?", font=("Arial", 40, "bold"))
question_label.pack()

image_folder = "images\\a_walk_in_the_park"
image_paths = get_image_paths(image_folder)

# Desired image size
image_size = (400, 400)

# Load images after initializing root window
images = load_images(image_paths, size=image_size)

# Creates unique one-by-one matching
image_pairs = list(combinations(images, 2))

# Initialize choice matrix
choice_matrix = {path: {} for path in image_paths}

# Ground image label
ground_image_path = "images\\a_walk_in_the_park\\a_walk_in_the_park_GT.jpg"
ground_image = load_images([ground_image_path], size=image_size)[0][0]
ground_image_label = tk.Label(root, image=ground_image)
ground_image_label.pack()

# Image labels for pairs
left_image_label = tk.Label(root, image=None)
left_image_label.pack(side="left")
left_image_label.bind("<Button-1>", lambda e: on_image_click(e, image_pairs[pair_index][0][1], image_pairs[pair_index][1][1]))

right_image_label = tk.Label(root, image=None)
right_image_label.pack(side="right")
right_image_label.bind("<Button-1>", lambda e: on_image_click(e, image_pairs[pair_index][1][1], image_pairs[pair_index][0][1]))

# Initialize the first pair
pair_index = -1
next_pair()

root.mainloop()
