import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

def train_task_scheduler_model(data_path='task_data.csv', model_path='task_scheduler_model.pkl'):
    data = pd.read_csv(data_path)
    features = data[['priority', 'stress_level', 'estimated_time', 'urgency']]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(scaled_features)

    joblib.dump(kmeans, model_path)
    joblib.dump(scaler, 'scaler.pkl')
    print("Model and scaler saved successfully.")

if __name__ == "__main__":
    train_task_scheduler_model()
