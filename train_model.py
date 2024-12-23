import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
import config

def train_user_embedding_model(data_path='data/user_questionnaire_data.csv', model_path=config.EMBEDDING_MODEL_PATH):
    """
    Trains an embedding model for users based on questionnaire data.
    This will use PCA to reduce the dimensionality of the user features to create user embeddings.
    """
    data = pd.read_csv(data_path)
    features = data[['hours_per_day', 'productive_time', 'break_frequency', 'wellness_activities']]
    
    # Convert categorical features to dummy variables
    features = pd.get_dummies(features, columns=['productive_time', 'break_frequency', 'wellness_activities'])
    
    # Save the columns for consistent encoding during inference
    feature_columns = features.columns
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Dimensionality reduction for embedding
    pca = PCA(n_components=2)
    user_embeddings = pca.fit_transform(scaled_features)
    
    # Save scaler, PCA model, and feature columns as a tuple
    joblib.dump((scaler, pca, feature_columns), model_path)
    print(f"User embedding model saved at {model_path}")

def train_task_priority_model(data_path='data/task_data.csv', model_path=config.TASK_PRIORITY_MODEL_PATH):
    data = pd.read_csv(data_path)
    features = data[['stress_level', 'deadline', 'estimated_time', 'category']]
    labels = data['priority_score']
    
    # Define the preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['category']),  # Updated to ignore unknowns
            ('num', StandardScaler(), ['stress_level', 'deadline', 'estimated_time'])
        ]
    )
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    
    pipeline.fit(features, labels)
    joblib.dump(pipeline, model_path)
    print(f"Task priority model saved at {model_path}")

def train_energy_prediction_model(data_path='data/energy_data.csv', model_path=config.ENERGY_PREDICTION_MODEL_PATH):
    data = pd.read_csv(data_path)
    features = data[['time_of_day', 'previous_day_energy', 'schedule_feedback']]
    labels = data['predicted_energy']
    
    # Preprocessing pipeline for numerical and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['previous_day_energy', 'schedule_feedback']),
            ('cat', OneHotEncoder(), ['time_of_day'])
        ]
    )
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    
    pipeline.fit(features, labels)
    joblib.dump(pipeline, model_path)
    print(f"Energy prediction model saved at {model_path}")

def train_time_slot_matching_model(data_path='data/time_slot_data.csv', model_path=config.TIME_SLOT_MATCHING_MODEL_PATH):
    data = pd.read_csv(data_path)
    features = data[['task_priority', 'energy_level']]
    labels = data['time_slot']
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])
    
    pipeline.fit(features, labels)
    joblib.dump(pipeline, model_path)
    print(f"Time slot matching model saved at {model_path}")

if __name__ == "__main__":
    # Paths to the training data
    user_questionnaire_data_path = 'data/user_questionnaire_data.csv'
    task_data_path = 'data/task_data.csv'
    energy_data_path = 'data/energy_data.csv'
    time_slot_data_path = 'data/time_slot_data.csv'
    
    # Train each model and save it
    train_user_embedding_model(data_path=user_questionnaire_data_path)
    train_task_priority_model(data_path=task_data_path)
    train_energy_prediction_model(data_path=energy_data_path)
    train_time_slot_matching_model(data_path=time_slot_data_path)
