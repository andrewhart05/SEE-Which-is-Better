
import tkinter as tk
from itertools import combinations
from PIL import Image, ImageTk
import csv

def load_images(image_paths, size=(300, 300)):
    images = []
    for path in image_paths:
        image = Image.open(path)
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        images.append((photo, path))  # Store the image along with its path
    return images

def next_pair():
    global pair_index
    pair_index += 1
    if pair_index >= len(image_pairs):
        save_clicks_to_csv()
        root.quit()
    else:
        update_images()

def update_images():
    left_image_label.config(image=image_pairs[pair_index][0][0])
    right_image_label.config(image=image_pairs[pair_index][1][0])

def on_image_click(event, image_path):
    click_counts[image_path] += 1
    next_pair()

def save_clicks_to_csv():
    with open('image_clicks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image', 'Clicks'])
        for path, count in click_counts.items():
            writer.writerow([path, count])

# Initialize Tkinter
root = tk.Tk()
root.title("Image Viewer")

# Image paths
image_paths = ["C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-10-01 221526.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-02 182412.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-02 182436.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-03 004711.png",
               "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-08 123200.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-12 192648.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-13 121931.png", "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-13 122028.png"]
ground_image_path = "C:\\Users\\andre\OneDrive\Pictures\Screenshots\Screenshot 2023-11-24 132511.png"

# Desired image size
image_size = (300, 300)

# Load images after initializing root window
images = load_images(image_paths, size=image_size)
ground_image = load_images([ground_image_path], size=image_size)[0][0]

# Create all unique pairs
image_pairs = list(combinations(images, 2))

# Initialize click counts
click_counts = {path: 0 for path in image_paths}

# Ground image label
ground_image_label = tk.Label(root, image=ground_image)
ground_image_label.pack()

# Image labels for pairs
left_image_label = tk.Label(root, image=None)
left_image_label.pack(side="left")
left_image_label.bind("<Button-1>", lambda e: on_image_click(e, image_pairs[pair_index][0][1]))

right_image_label = tk.Label(root, image=None)
right_image_label.pack(side="right")
right_image_label.bind("<Button-1>", lambda e: on_image_click(e, image_pairs[pair_index][1][1]))

# Initialize the first pair
pair_index = -1
next_pair()

# Start the application
root.mainloop()