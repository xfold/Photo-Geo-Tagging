import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json

class EmbeddingRetriever:
    def __init__(self, embeddings_df):
        """Initialize with a DataFrame containing image file paths and embeddings."""
        self.embeddings_df = embeddings_df
        self.embeddings = np.vstack(embeddings_df['embedding'].values)  # Convert embeddings from DataFrame to NumPy array

    def cosine_similarity(self, index, threshold=0.7, N=5):
        """Calculate cosine similarity and retrieve similar embeddings."""
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(self.embeddings)
        
        # Get similarities for the current embedding
        similarities = similarity_matrix[index]
        
        # Get indices of the most similar embeddings, sorted by similarity
        similar_indices = np.argsort(similarities)[::-1][1:]  # Skip the first one as it's the embedding itself

        # Filter by threshold
        filtered_indices = [i for i in similar_indices if similarities[i] >= threshold]

        # Get the top N similar embeddings above the threshold
        top_n_similar_indices = filtered_indices[:N]

        # Create a list of (image_path, similarity, embedding) triplets
        similar_images = []
        for idx in top_n_similar_indices:
            similar_images.append((
                self.embeddings_df.iloc[idx]['filepath'],
                float(similarities[idx]),
                self.embeddings_df.iloc[idx]['embedding']
            ))

        return similar_images

    def approximate_nearest_neighbors(self, index, N=10, threshold=0.95):
        """Retrieve similar embeddings using approximate nearest neighbors."""
        # Use NearestNeighbors from sklearn
        nbrs = NearestNeighbors(n_neighbors=N, algorithm='auto').fit(self.embeddings)
        distances, indices = nbrs.kneighbors(self.embeddings[index].reshape(1, -1))

        # Filter based on threshold
        filtered_triplets = []
        for i in range(len(indices[0])):
            dist = distances[0][i]
            if 1 - dist >= threshold:  # For cosine similarity interpretation
                filtered_triplets.append((
                    self.embeddings_df.iloc[indices[0][i]]['filepath'],
                    float(1 - dist),  # Convert distance to similarity
                    self.embeddings_df.iloc[indices[0][i]]['embedding']
                ))

        # Limit to N results
        filtered_triplets = filtered_triplets[:N]

        return filtered_triplets

    def find_similar_embeddings(self, input_value, method='cosine', N=10, threshold=0.95):
        """Retrieve similar embeddings based on the specified method."""
        # Determine index from input value
        if isinstance(input_value, int):
            index = input_value  # If input is an index
        elif isinstance(input_value, str):
            # If input is a filepath, locate the corresponding index
            try:
                index = self.embeddings_df[self.embeddings_df['filepath'] == input_value].index[0]
            except IndexError:
                raise ValueError(f"Image path '{input_value}' not found in the DataFrame.")
        else:
            raise ValueError("Input must be an index (int) or a file path (str).")

        # Call the appropriate similarity method
        if method == 'cosine':
            return self.cosine_similarity(index, threshold, N)
        elif method == 'nearest_neighbors':
            return self.approximate_nearest_neighbors(index, N, threshold)
        else:
            raise ValueError("Invalid method specified. Use 'cosine' or 'nearest_neighbors'.")
        
    def update_similar_images(self, method='cosine', N=10, threshold=0.95, output_file='data/similar_images.parquet'):
        """Iterate over all images and update the DataFrame with similar images."""
        similar_images_list = []
        for i in range(len(self.embeddings_df)):
            similar_images = self.find_similar_embeddings(i, method=method, N=N, threshold=threshold)
            # Collect similar images for this index
            similar_images_list.append( similar_images )

        # Update DataFrame with similar images
        self.embeddings_df['similar_images'] = similar_images_list
        self.embeddings_df['similar_images'] = self.embeddings_df['similar_images'].apply(lambda x: [k[0] for k in x])
        self.embeddings_df['threshold'] = threshold
        # Save the updated DataFrame to a Parquet file
        self.embeddings_df.to_parquet(output_file, index=False)
        print(f"Saved similar images in Parquet format to {output_file}.")
        return self.embeddings_df

