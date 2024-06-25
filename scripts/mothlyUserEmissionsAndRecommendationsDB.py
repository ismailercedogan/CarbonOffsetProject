import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

db_user = 'db'
db_password = 'db_pass'
db_host = 'localhost' 
db_name = 'hackathon'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

monthly_user_emissions_df = pd.read_csv('monthly_user_emissions.csv')
monthly_recommendations_df = pd.read_csv('monthly_recommendations.csv')

monthly_user_emissions_df.to_sql('monthly_user_emissions', con=engine, if_exists='replace', index=False)
monthly_recommendations_df.to_sql('monthly_recommendations', con=engine, if_exists='replace', index=False)

print("Monthly user emissions and recommendations loaded into the database.")

