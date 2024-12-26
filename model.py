import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the collected data
df = pd.read_csv('wumpus_game_data.csv')

# Normalize the data
scaler = StandardScaler()
data_normalized = scaler.fit_transform(df)

# Convert the data to a TensorFlow dataset
import tensorflow as tf

dataset = tf.data.Dataset.from_tensor_slices(data_normalized)
dataset = dataset.batch(len(data_normalized))  # Batch into one to feed the entire dataset

import tensorflow as tf
import numpy as np


class KMeansClustering:
    def __init__(self, n_clusters, n_features, n_iterations=100):
        self.n_clusters = n_clusters
        self.n_features = n_features
        self.n_iterations = n_iterations
        self.centroids = tf.Variable(tf.random.normal([n_clusters, n_features]))

    def fit(self, dataset):
        for _ in range(self.n_iterations):
            # Expand dimensions to make them compatible for broadcasting
            expanded_centroids = tf.expand_dims(self.centroids, 0)
            expanded_points = tf.expand_dims(dataset, 1)

            # Calculate distances and assign clusters
            distances = tf.reduce_sum(tf.square(expanded_points - expanded_centroids), axis=2)
            closest_cluster_indices = tf.argmin(distances, axis=1)

            # Update centroids
            for i in range(self.n_clusters):
                mask = tf.equal(closest_cluster_indices, i)
                assigned_points = tf.boolean_mask(dataset, mask)
                if tf.reduce_sum(mask) > 0:
                    new_centroid = tf.reduce_mean(assigned_points, axis=0)
                    self.centroids[i].assign(new_centroid)

        self.labels = closest_cluster_indices.numpy()
        return self.labels

    def predict(self, data_point):
        expanded_centroids = tf.expand_dims(self.centroids, 0)
        expanded_point = tf.expand_dims(data_point, 0)
        distances = tf.reduce_sum(tf.square(expanded_point - expanded_centroids), axis=2)
        return tf.argmin(distances, axis=1).numpy()[0]


# Apply K-Means with 3 clusters (for example)
n_clusters = 3
n_features = data_normalized.shape[1]
kmeans = KMeansClustering(n_clusters, n_features)

# Run K-Means clustering
labels = kmeans.fit(data_normalized)
df['cluster'] = labels

print(df.head())
