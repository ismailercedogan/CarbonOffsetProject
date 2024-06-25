import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

db_user = 'db'
db_password = 'db_pass'
db_host = 'localhost' 
db_name = 'hackathon'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

transactions_df = pd.read_sql('SELECT * FROM transactions', con=engine)
emission_factors_df = pd.read_sql('SELECT * FROM emission_factors', con=engine)

transactions_df['date'] = pd.to_datetime(transactions_df['date'])

transactions_df['emission'] = transactions_df.apply(
    lambda x: x['amount'] * emission_factors_df.loc[emission_factors_df['categoryName'] == x['category'], 'emissionFactor'].values[0],
    axis=1
)

monthly_user_emissions = transactions_df.groupby(['userId', transactions_df['date'].dt.to_period('M'), 'category'])['emission'].sum().reset_index()
monthly_user_emissions['date'] = monthly_user_emissions['date'].dt.to_timestamp('M') + pd.offsets.MonthEnd(0)

max_date = monthly_user_emissions['date'].max()
filtered_monthly_user_emissions = monthly_user_emissions[monthly_user_emissions['date'] < max_date]

# Save filtered monthly user emissions to CSV
filtered_monthly_user_emissions.to_csv('monthly_user_emissions.csv', index=False)
print("Filtered monthly user emissions calculated and saved to 'monthly_user_emissions.csv'.")



