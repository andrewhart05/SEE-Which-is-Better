import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Function to calculate expected probability
def calculate_expected_probability(rating_i, rating_j):
    return 1 / (1 + 10 ** ((rating_j - rating_i) / 400))

# Function to update ratings
def update_ratings(ratings, results, K):
    n = results.shape[0]  # Number of opponents based on the results matrix size
    for i in range(n):
        for j in range(i + 1, n):
            expected_prob_i_beats_j = calculate_expected_probability(ratings[i], ratings[j])
            expected_prob_j_beats_i = 1 - expected_prob_i_beats_j
            outcome_i_j = results[i, j]
            outcome_j_i = results[j, i]
            ratings[i] += K * (outcome_i_j - expected_prob_i_beats_j)
            ratings[j] += K * (outcome_j_i - expected_prob_j_beats_i)
    return ratings

# Function to read and prepare matrix from file
def read_and_prepare_matrix(file_path):
    df = pd.read_csv(file_path, index_col=0)
    objects = list(df.index)
    data_matrix = df.values
    return objects, data_matrix

# Main function to process files and update ratings
def process_files(files, K):
    initial_ratings = {}
    for file in files:
        objects, results_matrix = read_and_prepare_matrix(file)
        for obj in objects:
            if obj not in initial_ratings:
                initial_ratings[obj] = 1500.0  # Initial rating can be set as per requirement, e.g., 1500.0

        ratings_list = np.array([initial_ratings[obj] for obj in objects])
        updated_ratings = update_ratings(ratings_list, results_matrix, K)

        for i, obj in enumerate(objects):
            initial_ratings[obj] = updated_ratings[i]

    return initial_ratings

# Function to sort and normalize ratings
def sort_and_normalize_ratings(ratings):
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    ratings_only = [rating for _, rating in sorted_ratings]
    min_rating, max_rating = min(ratings_only), max(ratings_only)
    normalized_scores = [(obj, (rating - min_rating) / (max_rating - min_rating)) for obj, rating in sorted_ratings]
    return normalized_scores

# Function to create and return distance matrix
def create_distance_matrix(normalized_scores):
    normalized_scores_dict = dict(normalized_scores)
    objects_list = [obj for obj, _ in normalized_scores]
    n = len(normalized_scores)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i, j] = abs(normalized_scores_dict[objects_list[i]] - normalized_scores_dict[objects_list[j]])
    return distance_matrix, objects_list

# Function to plot ratings
def plot_ratings(objects, ratings, title="Ratings", xlabel="Objects", ylabel="Rating"):
    plt.figure(figsize=(12, 8))
    plt.bar(objects, ratings, color='skyblue')
    plt.xticks(rotation=90)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.show()
