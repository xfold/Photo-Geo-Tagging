from torchvision import models, transforms
from PIL import Image
import torch
import pandas as pd

class ImageEmbedder():
    def __init__(self):
        # Load pre-trained ResNet-50 model
        self.model = models.resnet50(pretrained=True)
        
        # Remove the final classification layer (fully connected layer)
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])  # Remove the last layer
        
        self.model.eval()  # Set model to evaluation mode

        # Define image transformations (resize, normalize to match model expectations)
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Initialize an empty DataFrame to keep track of file paths and embeddings
        self.embeddings_df = pd.DataFrame(columns=['filepath', 'embedding'])

    # Function to calculate embedding for a single image
    def get_embedding(self, image_path, save_embedding=True):
        # Check if embedding already exists for this image
        if image_path in self.embeddings_df['filepath'].values:
            print(f"Embedding already exists for {image_path}.")
            return self.embeddings_df.loc[self.embeddings_df['filepath'] == image_path, 'embedding'].values[0]

        # Load and preprocess the image
        image = Image.open(image_path).convert('RGB')
        image = self.preprocess(image).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            embedding = self.model(image).squeeze().numpy()  # Remove unnecessary dimensions and convert to NumPy array
        
        # Use pd.concat to add the new DataFrame to the existing one
        if(save_embedding):
            new_embedding_df = pd.DataFrame({'filepath': [image_path], 'embedding': [embedding]})
            self.embeddings_df = pd.concat([self.embeddings_df, new_embedding_df], ignore_index=True)
        
        return embedding

    def save_embeddings(self, save_path):
        # Save the embeddings DataFrame to a Parquet file
        self.embeddings_df.to_parquet(save_path, index=False)
        print(f"Saved {len(self.embeddings_df)} embeddings in Parquet format to {save_path}.")


