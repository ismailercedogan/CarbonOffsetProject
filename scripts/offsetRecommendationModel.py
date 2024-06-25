import pandas as pd
from sqlalchemy import create_engine
from sklearn.neighbors import NearestNeighbors
import joblib
import random

db_user = 'db'
db_password = 'db_pass'
db_host = 'localhost' 
db_name = 'hackathon'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Load monthly recommendations from the database
monthly_recommendations_df = pd.read_sql('SELECT * FROM monthly_recommendations', con=engine)

# Create a pivot table for collaborative filtering
user_project_matrix = monthly_recommendations_df.pivot_table(index='userId', columns='project', values='rating', fill_value=0)

# Train a collaborative filtering model (user-based KNN)
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(user_project_matrix.values)


joblib.dump(model, 'offset_recommendation_model.pkl')
joblib.dump(user_project_matrix, 'user_project_matrix.pkl')
print("Recommendation model trained and saved.")
