import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

def train_embedding_model(data_path='user_questionnaire_data.csv', model_path='data/user_embeddings.pkl'):
    data = pd.read_csv(data_path)
    features = data[['hours_per_day', 'productive_time', 'break_frequency', 'wellness_activities']]
    features = pd.get_dummies(features, columns=['productive_time', 'break_frequency', 'wellness_activities'])
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    pca = PCA(n_components=2)
    embeddings = pca.fit_transform(scaled_features)
    
    joblib.dump((pca, scaler), model_path)
    print("User embedding model saved successfully.")

if __name__ == "__main__":
    train_embedding_model()
