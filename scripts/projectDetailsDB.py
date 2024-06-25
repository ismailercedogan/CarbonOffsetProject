import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random


db_user = 'db'
db_password = 'db_pass'
db_host = 'localhost' 
db_name = 'hackathon'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Define detailed carbon offset projects
project_details = [
    {"projectId": Faker().uuid4(), "projectName": "Landfill Gas Capture", "category": "Groceries", "description": "Capture and destroy landfill gas to reduce methane emissions."},
    {"projectId": Faker().uuid4(), "projectName": "Biogas from Waste", "category": "Groceries", "description": "Produce biogas from organic waste."},
    {"projectId": Faker().uuid4(), "projectName": "Efficient Cookstoves", "category": "Restaurant", "description": "Distribute efficient cookstoves to reduce fuel use and emissions."},
    {"projectId": Faker().uuid4(), "projectName": "Public Transport Enhancement", "category": "Public Transport", "description": "Improve public transport infrastructure to reduce emissions."},
    {"projectId": Faker().uuid4(), "projectName": "Methane Capture from Livestock", "category": "Fuel", "description": "Capture and destroy methane from livestock manure."},
    {"projectId": Faker().uuid4(), "projectName": "Coal Mine Methane Capture", "category": "Fuel", "description": "Capture and utilize methane from coal mines."},
    {"projectId": Faker().uuid4(), "projectName": "Educational Infrastructure", "category": "Education", "description": "Build sustainable educational facilities."},
    {"projectId": Faker().uuid4(), "projectName": "Healthcare Facilities", "category": "Health", "description": "Improve energy efficiency in healthcare facilities."},
    {"projectId": Faker().uuid4(), "projectName": "Avoided Deforestation", "category": "Books", "description": "Prevent deforestation to sequester carbon."},
    {"projectId": Faker().uuid4(), "projectName": "Improved Forest Management", "category": "Books", "description": "Manage forests to improve carbon sequestration."},
    {"projectId": Faker().uuid4(), "projectName": "Solar/Wind Energy", "category": "Entertainment", "description": "Install solar panels and wind turbines."},
    {"projectId": Faker().uuid4(), "projectName": "Renewable Energy Projects", "category": "Entertainment", "description": "Invest in renewable energy projects."},
    {"projectId": Faker().uuid4(), "projectName": "Food Waste Reduction", "category": "Groceries", "description": "Reduce food waste through better management and redistribution."},
    {"projectId": Faker().uuid4(), "projectName": "Restaurant Sustainability", "category": "Restaurant", "description": "Implement sustainable practices in restaurants."},
    {"projectId": Faker().uuid4(), "projectName": "Green Urban Planning", "category": "Public Transport", "description": "Develop green urban areas to reduce emissions."},
    {"projectId": Faker().uuid4(), "projectName": "Fuel Efficiency Projects", "category": "Fuel", "description": "Increase fuel efficiency in vehicles."},
    {"projectId": Faker().uuid4(), "projectName": "School Energy Efficiency", "category": "Education", "description": "Improve energy efficiency in schools."},
    {"projectId": Faker().uuid4(), "projectName": "Hospital Energy Efficiency", "category": "Health", "description": "Improve energy efficiency in hospitals."},
    {"projectId": Faker().uuid4(), "projectName": "Paper Recycling Projects", "category": "Books", "description": "Promote paper recycling to reduce deforestation."},
    {"projectId": Faker().uuid4(), "projectName": "Green Event Planning", "category": "Entertainment", "description": "Plan events with minimal environmental impact."}
]

project_details_df = pd.DataFrame(project_details)

project_details_df.to_sql('project_details', con=engine, if_exists='replace', index=False)
print("Project details saved to database.")
