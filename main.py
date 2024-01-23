import os
import random
from PIL import Image, ImageTk
import tkinter as tk

class ImageDisplayApp:
    def __init__(self, master, image_folder):
        self.master = master
        self.master.title("Random Image Display")
        self.image_folder = image_folder
        self.window_width = 800
        self.window_height = 600

        # Initialize label_left and label_right attributes
        self.label_left = None
        self.label_right = None

        self.display_images()

    def choose_random_images(self, num_images=2):
        all_files = os.listdir(self.image_folder)
        image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        chosen_images = random.sample(image_files, min(num_images, len(image_files)))
        return chosen_images

    def calculate_optimal_size(self, image_width, image_height):
        width_ratio = self.window_width / (2 * image_width)
        height_ratio = self.window_height / image_height
        min_ratio = min(width_ratio, height_ratio)
        new_width = int(image_width * min_ratio)
        new_height = int(image_height * min_ratio)
        return new_width, new_height

    def display_images(self):
        chosen_images = self.choose_random_images(num_images=2)

        image_left = Image.open(os.path.join(self.image_folder, chosen_images[0]))
        image_right = Image.open(os.path.join(self.image_folder, chosen_images[1]))

        optimal_size_left = self.calculate_optimal_size(image_left.width, image_left.height)
        optimal_size_right = self.calculate_optimal_size(image_right.width, image_right.height)

        image_left = image_left.resize(optimal_size_left)
        image_right = image_right.resize(optimal_size_right)

        photo_left = ImageTk.PhotoImage(image_left)
        photo_right = ImageTk.PhotoImage(image_right)

        # Check if labels are not None before destroying
        if self.label_left:
            self.label_left.destroy()
        if self.label_right:
            self.label_right.destroy()

        # Create new buttons for the new images
        self.label_left = tk.Button(self.master, image=photo_left, command=lambda: self.on_image_click(chosen_images))
        self.label_right = tk.Button(self.master, image=photo_right, command=lambda: self.on_image_click(chosen_images))

        self.label_left.photo = photo_left
        self.label_right.photo = photo_right

        self.label_left.pack(side=tk.LEFT)
        self.label_right.pack(side=tk.LEFT)

    def on_image_click(self, previous_images):
        # Destroy the existing labels
        if self.label_left:
            self.label_left.destroy()
        if self.label_right:
            self.label_right.destroy()

        # Choose two new random images
        new_images = self.choose_random_images(num_images=2)

        image_left = Image.open(os.path.join(self.image_folder, new_images[0]))
        image_right = Image.open(os.path.join(self.image_folder, new_images[1]))

        optimal_size_left = self.calculate_optimal_size(image_left.width, image_left.height)
        optimal_size_right = self.calculate_optimal_size(image_right.width, image_right.height)

        image_left = image_left.resize(optimal_size_left)
        image_right = image_right.resize(optimal_size_right)

        photo_left = ImageTk.PhotoImage(image_left)
        photo_right = ImageTk.PhotoImage(image_right)

        # Create new buttons for the new images
        self.label_left = tk.Button(self.master, image=photo_left, command=lambda: self.on_image_click(new_images))
        self.label_right = tk.Button(self.master, image=photo_right, command=lambda: self.on_image_click(new_images))

        self.label_left.photo = photo_left
        self.label_right.photo = photo_right

        self.label_left.pack(side=tk.LEFT)
        self.label_right.pack(side=tk.LEFT)

# Replace 'path_to_your_images_folder' with the actual folder path containing your images
image_folder = "\"

# Create the main window
root = tk.Tk()

# Create the app instance
app = ImageDisplayApp(root, image_folder)

# Run the main loop
root.mainloop()
