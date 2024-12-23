import joblib
from .db import get_db_connection
from .user_embeddings import create_user_embedding, cluster_user

def save_user_profile(user_data):
    # Generate embedding and determine cluster
    embedding = create_user_embedding(user_data)
    user_cluster = cluster_user(embedding)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (email, cluster)
        VALUES (?, ?)
    ''', (user_data['email'], user_cluster))
    conn.commit()
    conn.close()
    return user_cluster
