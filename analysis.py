import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# image = "Waterbottle"

def calculate_expected_probability(rating_i, rating_j):
    return 1 / (1 + 10 ** ((rating_j - rating_i) / 400))

def update_ratings(ratings, results, K):
    n = results.shape[0]  # Number of opponents based on the results matrix size
    for i in range(n):
        for j in range(i + 1, n):
            expected_prob_i_beats_j = calculate_expected_probability(ratings[i], ratings[j])
            expected_prob_j_beats_i = 1 - expected_prob_i_beats_j
            # Update ratings based on the result matrix
            outcome_i_j = results[i, j]  # Outcome of i vs j
            outcome_j_i = results[j, i]  # Outcome of j vs i (should complement the above)
            ratings[i] += K * (outcome_i_j - expected_prob_i_beats_j)
            ratings[j] += K * (outcome_j_i - expected_prob_j_beats_i)
    return ratings

def read_and_prepare_matrix(file_path):
    df = pd.read_csv(file_path, index_col=0)  # Assuming the first column is an index or identifier
    objects = list(df.index)  # Extract object names
    data_matrix = df.values  # Use values directly for the numpy array
    return objects, data_matrix

# files = [
#     f"Results/Dirk_{image}_choices_matrix.csv",
#     f"Results/Maryam_{image}_choices_matrix.csv",
#     f"Results/Nathan_{image}_choices_matrix.csv",
#     f"Results/Doruk_{image}_choices_matrix.csv",
#     f"Results/Andrew_{image}_choices_matrix.csv"
# ]

# K = 32
# initial_ratings = {}  # Initialize an empty dictionary for ratings

# for file in files:
#     objects, results_matrix = read_and_prepare_matrix(file)
#     # Initialize or update ratings for objects
#     for obj in objects:
#         if obj not in initial_ratings:
#             initial_ratings[obj] = 0.0  # Start with a base rating for new objects

#     # Prepare the ratings list in the order of objects for this file
#     ratings_list = np.array([initial_ratings[obj] for obj in objects])

#     # Update ratings based on this file's results
#     updated_ratings = update_ratings(ratings_list, results_matrix, K)

#     # Update the global ratings dictionary
#     for i, obj in enumerate(objects):
#         initial_ratings[obj] = updated_ratings[i]

# # Convert ratings to a sorted list for visualization and analysis
# sorted_ratings = sorted(initial_ratings.items(), key=lambda x: x[1], reverse=True)

# # Plotting the final ratings
# plt.figure(figsize=(12, 8))
# objects, ratings = zip(*sorted_ratings)
# plt.bar(objects, ratings)
# plt.xticks(rotation=90)
# plt.title("ELO Ratings of Opponents")
# plt.ylabel("ELO Rating")
# plt.show()

# # Print the ELO scores
# print("ELO Scores before normalization:")
# for obj, rating in sorted_ratings:
#     print(f"{obj}: {rating}")

# # Normalize the scores
# ratings_only = [rating for _, rating in sorted_ratings]
# min_rating = min(ratings_only)
# max_rating = max(ratings_only)
# normalized_scores = [(obj, (rating - min_rating) / (max_rating - min_rating)) for obj, rating in sorted_ratings]

# # Print the normalized scores
# print("\nNormalized ELO Scores (0 to 1 scale):")
# for obj, normalized_score in normalized_scores:
#     print(f"{obj}: {normalized_score:.3f}")

# # Assuming normalized_scores is a list of tuples (object, normalized_score)
# normalized_scores_dict = dict(normalized_scores)

# # Create a list of objects to maintain order
# objects_list = [obj for obj, _ in normalized_scores]

# # Initialize an empty matrix
# n = len(normalized_scores)
# distance_matrix = np.zeros((n, n))

# # Populate the distance matrix
# for i in range(n):
#     for j in range(n):
#         distance_matrix[i, j] = normalized_scores_dict[objects_list[i]] - normalized_scores_dict[objects_list[j]]

# # Display the distance matrix
# print("\nDistance Matrix:")
# print(distance_matrix)

# # Plotting the normalized ELO scores
# plt.figure(figsize=(12, 8))
# objects, normalized_ratings = zip(*normalized_scores)  # Unpack the objects and their normalized scores
# plt.bar(objects, normalized_ratings, color='skyblue')
# plt.xticks(rotation=90)
# plt.title("Normalized ELO Scores")
# plt.ylabel("Normalized Score")
# plt.xlabel("Objects")
# plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
# plt.show()

# # Convert the distance matrix to a DataFrame
# distance_df = pd.DataFrame(distance_matrix, index=objects_list, columns=objects_list)

# # Output the DataFrame to a CSV file
# csv_file_path = f'{image}_distance_matrix.csv'
# distance_df.to_csv(csv_file_path)
