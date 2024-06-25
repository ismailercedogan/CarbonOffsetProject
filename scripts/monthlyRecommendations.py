import pandas as pd
import random
from faker import Faker

fake = Faker()

# Load the filtered monthly user emissions
monthly_user_emissions = pd.read_csv('monthly_user_emissions.csv')

# Define the mapping between transaction categories and carbon offset projects
transaction_to_offset_mapping = {
    "Groceries": ["Landfill Gas Capture", "Biogas from Waste", "Food Waste Reduction"],
    "Restaurant": ["Efficient Cookstoves", "Biogas from Waste", "Restaurant Sustainability"],
    "Public Transport": ["Public Transport Enhancement", "Green Urban Planning"],
    "Fuel": ["Methane Capture from Livestock", "Coal Mine Methane Capture", "Fuel Efficiency Projects"],
    "Education": ["Educational Infrastructure", "School Energy Efficiency"],
    "Health": ["Healthcare Facilities", "Hospital Energy Efficiency"],
    "Books": ["Avoided Deforestation", "Improved Forest Management", "Paper Recycling Projects"],
    "Entertainment": ["Solar/Wind Energy", "Renewable Energy Projects", "Green Event Planning"]
}

# Define detailed carbon offset projects
carbon_offset_projects = {
    "Landfill Gas Capture": "Capture and destroy landfill gas to reduce methane emissions.",
    "Biogas from Waste": "Produce biogas from organic waste.",
    "Efficient Cookstoves": "Distribute efficient cookstoves to reduce fuel use and emissions.",
    "Public Transport Enhancement": "Improve public transport infrastructure to reduce emissions.",
    "Methane Capture from Livestock": "Capture and destroy methane from livestock manure.",
    "Coal Mine Methane Capture": "Capture and utilize methane from coal mines.",
    "Educational Infrastructure": "Build sustainable educational facilities.",
    "Healthcare Facilities": "Improve energy efficiency in healthcare facilities.",
    "Avoided Deforestation": "Prevent deforestation to sequester carbon.",
    "Improved Forest Management": "Manage forests to improve carbon sequestration.",
    "Solar/Wind Energy": "Install solar panels and wind turbines.",
    "Renewable Energy Projects": "Invest in renewable energy projects.",
    "Food Waste Reduction": "Reduce food waste through better management and redistribution.",
    "Restaurant Sustainability": "Implement sustainable practices in restaurants.",
    "Green Urban Planning": "Develop green urban areas to reduce emissions.",
    "Fuel Efficiency Projects": "Increase fuel efficiency in vehicles.",
    "School Energy Efficiency": "Improve energy efficiency in schools.",
    "Hospital Energy Efficiency": "Improve energy efficiency in hospitals.",
    "Paper Recycling Projects": "Promote paper recycling to reduce deforestation.",
    "Green Event Planning": "Plan events with minimal environmental impact."
}


# Create a function to generate monthly recommendations
def generate_monthly_recommendations(monthly_user_emissions, transaction_to_offset_mapping, carbon_offset_projects):
    monthly_recommendations = []

    for (user_id, date), group in monthly_user_emissions.groupby(['userId', 'date']):
        # Find the category with the highest emission for the user in the given month
        top_category = group.sort_values(by='emission', ascending=False).iloc[0]['category']
        project_options = transaction_to_offset_mapping[top_category]
        selected_project = random.choice(project_options)
        recommendation = {
            'userId': user_id,
            'date': date,
            'project': selected_project,
            'category': top_category,
            'description': carbon_offset_projects[selected_project],
            'rating': random.randint(1, 5)
        }
        monthly_recommendations.append(recommendation)

    return pd.DataFrame(monthly_recommendations)

monthly_recommendations_df = generate_monthly_recommendations(monthly_user_emissions, transaction_to_offset_mapping, carbon_offset_projects)


monthly_recommendations_df.to_csv('monthly_recommendations.csv', index=False)
print("Monthly recommendations generated and saved to 'monthly_recommendations.csv'.")
