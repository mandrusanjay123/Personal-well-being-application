import joblib
import pandas as pd
from config import EMBEDDING_MODEL_PATH

# Load pre-trained embedding model, including scaler, PCA, and feature columns
scaler, pca, feature_columns = joblib.load(EMBEDDING_MODEL_PATH)

def create_user_embedding(user_data):
    """
    Creates an embedding for the user based on questionnaire data.
    
    Parameters:
        - user_data (dict): Dictionary containing user attributes.
        
    Returns:
        - embedding (numpy array): 2-dimensional embedding for the user.
    """
    # Prepare data for embedding, excluding non-numeric fields like 'email'
    user_df = pd.DataFrame([user_data])
    user_df = user_df.drop(columns=['email'])  # Exclude the email field
    
    # Convert categorical features to dummy variables
    user_df = pd.get_dummies(user_df, columns=['productive_time', 'break_frequency', 'wellness_activities'])
    
    # Align with training columns, add missing columns as zeros
    for col in feature_columns:
        if col not in user_df.columns:
            user_df[col] = 0
    user_df = user_df[feature_columns]  # Reorder columns to match training order
    
    # Transform using scaler and PCA
    user_vector = scaler.transform(user_df)
    embedding = pca.transform(user_vector)
    return embedding

def cluster_user(embedding):
    # Simple rule for clustering, adjust if using k-means, etc.
    return "morning_person" if embedding[0][0] < 0 else "night_owl"