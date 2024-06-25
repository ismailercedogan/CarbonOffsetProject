# Carbon Offset Project

## Overview
This project aims to develop a comprehensive application that calculates carbon emissions based on user transactions, provides carbon offset recommendations, and tracks user ratings of those recommendations. The application consists of a Flask-based backend and a React-based frontend.

## Table of Contents
- [Carbon Offset Project](#carbon-offset-project)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
  - [Data Generation](#data-generation)
    - [Generating Users and Transactions](#generating-users-and-transactions)
    - [Generating Emissions and Recommendations](#generating-emissions-and-recommendations)
    - [Loading Data into Database](#loading-data-into-database)
  - [Running the Application](#running-the-application)
  - [Using the Application](#using-the-application)
    - [Login](#login)
    - [Dashboard](#dashboard)
    - [Emission History](#emission-history)
    - [Expenses](#expenses)

## Prerequisites
- Python 3.7+
- Node.js 14+
- MySQL

## Setup Instructions
### Backend Setup
1. Clone the repository:
     ```
     git clone https://github.com/your-repo/hackathon_project.git
     cd hackathon_project/backend
     ```

2. Create and activate a virtual environment:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

3. Install dependencies:
     ```
     pip install -r requirements.txt
     ```

4. Setup MySQL database:
     - Create a database named `hackathon`.
     - Update the database credentials in the scripts (if different from defaults).

5. Run the following scripts to generate and load data:
     ```
     python transactions.py
     python transactionsDB.py
     python monthlyUserEmissions.py
     python monthlyRecommendations.py
     python monthlyUserEmissionsAndRecommendationsDB.py
     python projectDetailsDB.py
     python offsetRecommendationModel.py
     ```

6. Start the backend server:
     ```
     flask run
     ```

### Frontend Setup
1. Navigate to the frontend directory:
     ```
     cd ../frontend
     ```

2. Install dependencies:
     ```
     npm install
     ```

3. Start the frontend server:
     ```
     npm start
     ```

## Data Generation
### Generating Users and Transactions
The `transactions.py` script generates synthetic user data and transactions based on predefined spending patterns and emission factors. The generated data is saved as CSV files (`users.csv`, `transactions.csv`, `emission_factors.csv`).

### Generating Emissions and Recommendations
The `monthlyUserEmissions.py` script calculates monthly user emissions based on transaction data and emission factors. The results are saved to `monthly_user_emissions.csv`.

The `monthlyRecommendations.py` script generates carbon offset project recommendations based on user emissions. The results are saved to `monthly_recommendations.csv`.

### Loading Data into Database
The `transactionsDB.py`, `monthlyUserEmissionsAndRecommendationsDB.py`, and `projectDetailsDB.py` scripts load the generated data into a MySQL database.

## Running the Application
1. Start the backend server:
     ```
     cd backend
     `venv\Scripts\activate`  # On Linux use source venv/bin/activate 
     flask run
     ```

2. Start the frontend server:
     ```
     cd ../frontend
     npm start
     ```

3. Access the application:
     Open a web browser and go to http://localhost:3000.

## Using the Application

### Login

The Login page allows users to log in to access their personalized dashboard, emission history, and expenses.

![Login](/data/Login.png)

### Dashboard
The Dashboard provides a summary of the user's carbon emissions, displays a pie chart of the emissions by category, and allows the user to generate and apply carbon offset recommendations.

![Dashboard](/data/Dashboard.png)

### Emission History
The Emission History page shows the user's historical emissions and the recommendations provided for each month. Emissions and recommendations are displayed side-by-side for easy comparison.

![EmissionHistory](/data/EmissionHistory.png)

### Expenses
The Expenses page provides a breakdown of the user's spending by category for each month. Users can select a month to view detailed expenses.

![Expenses](/data/Expenses.png)

