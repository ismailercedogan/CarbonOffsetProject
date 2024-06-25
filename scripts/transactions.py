from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker()

# Define real emission factors per Turkish Lira spent
real_emission_factors = {
    "Groceries": 0.0126,
    "Restaurant": 0.0126,
    "Public Transport": 0.005,
    "Fuel": 0.04,
    "Education": 0.0045,
    "Health": 0.009,
    "Books": 0.006,
    "Entertainment": 0.0105
}

# Predefined MCC codes and categories
mcc_codes = [
    {"mcc": "5411", "category": "Groceries"},
    {"mcc": "5812", "category": "Restaurant"},
    {"mcc": "4111", "category": "Public Transport"},
    {"mcc": "5541", "category": "Fuel"},
    {"mcc": "8220", "category": "Education"},
    {"mcc": "5912", "category": "Health"},
    {"mcc": "5942", "category": "Books"},
    {"mcc": "7997", "category": "Entertainment"}
]

spending_distribution = {
    "Groceries": (0.10, 0.15),
    "Public Transport": (0.05, 0.08),
    "Fuel": (0.05, 0.10),
    "Restaurant": (0.05, 0.10),
    "Education": (0.05, 0.10),
    "Health": (0.05, 0.10),
    "Books": (0.01, 0.03),
    "Entertainment": (0.03, 0.05)
}

transaction_ranges = {
    "Groceries": (200, 1000),
    "Restaurant": (200, 8000),
    "Public Transport": (10, 500),
    "Fuel": (100, 1000),
    "Education": (2000, 200000),
    "Health": (50, 1000),
    "Books": (100, 2000),
    "Entertainment": (500, 10000)
}


def generate_users(num_users):
    users = []
    for _ in range(num_users):
        income = round(random.uniform(240000, 3000000), 2)  # Annual income
        credit_card_limit = round(income * random.uniform(0.1, 0.3), 2)  # Credit card limit as 10-30% of annual income
        user = {
            'userId': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'passwordHash': fake.password(),
            'age': random.randint(18, 70),
            'income': income,
            'creditCardLimit': credit_card_limit,
            'financialGoals': fake.sentence(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'accountCreationDate': fake.date_this_decade()
        }
        users.append(user)
    return users

# Generate synthetic transactions with realistic spending patterns distributed over 3 months
def generate_transactions(num_transactions_per_month, users):
    transactions = []
    start_date = fake.date_this_year() - timedelta(days=90) 
    for user in users:
        for month in range(3):  
            available_credit = user['creditCardLimit']
            for category, (min_percentage, max_percentage) in spending_distribution.items():
                category_spending = round(random.uniform(min_percentage, max_percentage) * available_credit, 2)
                num_category_transactions = num_transactions_per_month // len(spending_distribution)
                for _ in range(num_category_transactions):
                    min_amount, max_amount = transaction_ranges[category]
                    amount = round(random.uniform(min_amount, max_amount), 2)
                    if available_credit - amount < 0:
                        break
                    mcc = next(item['mcc'] for item in mcc_codes if item["category"] == category)
                    transaction_date = start_date + timedelta(days=month * 30 + random.randint(0, 29))  # Distribute over 3 months
                    transaction = {
                        'transactionId': fake.uuid4(),
                        'userId': user['userId'],  # Link transaction to user
                        'date': transaction_date,
                        'description': fake.sentence(),
                        'amount': amount,
                        'category': category,
                        'mcc': mcc,
                        'merchantName': fake.company(),
                        'merchantCity': fake.city(),
                        'merchantCountry': fake.country(),
                        'paymentMethod': 'Credit Card'
                    }
                    transactions.append(transaction)
                    available_credit -= amount
                    if available_credit <= 0:
                        break
    return transactions


def get_real_emission_factors():
    return [
        {"categoryId": fake.uuid4(), "categoryName": category, "emissionFactor": factor}
        for category, factor in real_emission_factors.items()
    ]


# Generate data
num_users = 100
num_transactions_per_month = 200

users = generate_users(num_users)
transactions = generate_transactions(num_transactions_per_month, users)
emission_factors = get_real_emission_factors()

# Convert to DataFrames for easy manipulation
users_df = pd.DataFrame(users)
transactions_df = pd.DataFrame(transactions)
emission_factors_df = pd.DataFrame(emission_factors)


users_df.to_csv('users.csv', index=False)
transactions_df.to_csv('transactions.csv', index=False)
emission_factors_df.to_csv('emission_factors.csv', index=False)

print("Synthetic data generated and saved to CSV files.")
