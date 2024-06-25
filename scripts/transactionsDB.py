import pandas as pd
from sqlalchemy import create_engine


db_user = 'db'
db_password = 'db_pass'
db_host = 'localhost' 
db_name = 'hackathon'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

users_df = pd.read_csv('hackathon/users.csv')
transactions_df = pd.read_csv('hackathon/transactions.csv')
emission_factors_df = pd.read_csv('hackathon/emission_factors.csv')

users_df.to_sql('users', con=engine, if_exists='append', index=False)
transactions_df.to_sql('transactions', con=engine, if_exists='append', index=False)
emission_factors_df.to_sql('emission_factors', con=engine, if_exists='append', index=False)

print("Data loaded successfully into MySQL database.")
