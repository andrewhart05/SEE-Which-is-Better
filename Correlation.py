import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from Fitness import FF_ML2DHD_V2, FF_Gamma, FF_Hamming, FF_ML2DHD
import os
import imageio.v2 as imageio


def preprocess_image(image):
    """Convert RGBA images to RGB by discarding the alpha channel."""
    if image.shape[-1] == 4:  # Check if the image has 4 channels
        return image[..., :3]  # Discard the alpha channel
    return image


def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if
                   os.path.isfile(os.path.join(folder_path, f)) and not f.endswith(
                       ('og.jpg', 'og.jpeg', 'og.png')) and f.lower().endswith(('jpg', 'jpeg', 'png'))]

    if not image_files:
        print("No images found to process.")
        return

    print(f"Processing {len(image_files)} images...")

    functions = [FF_ML2DHD_V2, FF_Gamma, FF_Hamming, FF_ML2DHD]

    for function in functions:
        n = len(image_files)
        distance_matrix = np.zeros((n, n))

        for i, file1 in enumerate(image_files):
            image1_path = os.path.join(folder_path, file1)
            image1 = preprocess_image(imageio.imread(image1_path))
            for j, file2 in enumerate(image_files):
                if i != j:  # Ensure unique pairs
                    image2_path = os.path.join(folder_path, file2)
                    image2 = preprocess_image(imageio.imread(image2_path))
                    distance_matrix[i][j] = function(image1, image2)[
                        0]  # Assuming the first element is the desired score

        # Convert the distance matrix to a DataFrame and save to CSV
        df = pd.DataFrame(distance_matrix, index=image_files, columns=image_files)
        csv_path = os.path.join(folder_path, f"{function.__name__}_distance_matrix.csv")
        df.to_csv(csv_path)
        print(f"Saved {csv_path}")


def plot_regression(independent_csv, dependent_csvs, labels):
    df_independent = pd.read_csv(independent_csv, index_col=0)
    independent_flat = df_independent.values.flatten()

    plt.figure(figsize=(10, 7))

    for i, (dependent_csv, label) in enumerate(zip(dependent_csvs, labels)):
        df_dependent = pd.read_csv(dependent_csv, index_col=0)
        dependent_flat = df_dependent.values.flatten()

        X = sm.add_constant(independent_flat)
        model = sm.OLS(dependent_flat, X).fit()
        x_pred = np.linspace(independent_flat.min(), independent_flat.max(), 50)
        y_pred = model.params[0] + model.params[1] * x_pred

        plt.scatter(independent_flat, dependent_flat, label=f'{label}')
        plt.plot(x_pred, y_pred, lw=2)

        # Equation and R^2 for annotation
        eq_text = f'{label}: y = {model.params[1]:.4f}x + {model.params[0]:.4f}\n$R^2$ = {model.rsquared:.2f}'

        # Place text on the plot
        plt.text(0.05, 0.95 - i * 0.06, eq_text, transform=plt.gca().transAxes, fontsize=9, verticalalignment='top')

    plt.xlabel('Elo Distance')
    plt.ylabel('Fitness Function Distances')
    plt.title('Linear Regression - Mushrooms')
    plt.legend()
    plt.show()


def perform_regression_significance_test(independent_csv, dependent_csvs, labels):
    # Load the independent variable distance matrix
    df_independent = pd.read_csv(independent_csv, index_col=0)
    independent_flat = df_independent.values.flatten()

    # Iterate through each dependent variable (fitness function distance matrix)
    for dependent_csv, label in zip(dependent_csvs, labels):
        # Load the dependent variable distance matrix
        df_dependent = pd.read_csv(dependent_csv, index_col=0)
        dependent_flat = df_dependent.values.flatten()

        # Prepare data for regression analysis
        X = sm.add_constant(independent_flat)  # Adds a constant term to the predictor
        y = dependent_flat

        # Perform linear regression
        model = sm.OLS(y, X).fit()

        # Extract and print the results
        print(f"Results for {label}:")
        print(f"Coefficient (slope): {model.params[1]}, p-value: {model.pvalues[1]}")
        print(f"Intercept: {model.params[0]}, p-value: {model.pvalues[0]}")
        print(f"R-squared: {model.rsquared}")
        print(f"---")


# Example usage parameters (make sure to replace these with actual file paths)
independent_csv = 'Analysis/Waterbottle_Elo_abs_distance_matrix.csv'
dependent_csvs = ['Analysis/Waterbottle_FF_ML2DHD_V2_distance_matrix.csv', 'Analysis/Waterbottle_FF_Gamma_distance_matrix.csv', 'Analysis/Waterbottle_FF_Hamming_distance_matrix.csv',
                  'Analysis/Waterbottle_FF_ML2DHD_distance_matrix.csv']
labels = ['FF_ML2DHD_V2', 'FF_Gamma', 'FF_Hamming', 'FF_ML2DHD']  # Example function names or labels

#plot_regression(independent_csv, dependent_csvs, labels)
perform_regression_significance_test(independent_csv, dependent_csvs, labels)


