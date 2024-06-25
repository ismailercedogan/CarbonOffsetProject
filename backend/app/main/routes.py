from . import main
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Transactions, MonthlyUserEmissions, MonthlyRecommendations, ProjectDetails, EmissionFactors
from app import db
from datetime import datetime
import joblib

@main.route('/calculate-emissions', methods=['GET'])
@jwt_required()
def calculate_emissions():
    user_id = get_jwt_identity()

    current_month = datetime.now().strftime('%Y-%m')

    existing_emissions = MonthlyUserEmissions.query.filter_by(userId=user_id, date=datetime.strptime(current_month, '%Y-%m')).all()
    
    if existing_emissions:
        monthly_emissions = {current_month: [
            {"category": e.category, "emission": e.emission} for e in existing_emissions
        ]}
    else:
        transactions = Transactions.query.filter_by(userId=user_id).filter(Transactions.date.startswith(current_month)).all()
        emission_factors = {ef.categoryName: ef.emissionFactor for ef in EmissionFactors.query.all()}

        monthly_emissions = {}
        for transaction in transactions:
            month = transaction.date.strftime('%Y-%m')
            if month not in monthly_emissions:
                monthly_emissions[month] = []
            emission_value = transaction.amount * emission_factors.get(transaction.category, 0)
            monthly_emissions[month].append({"category": transaction.category, "emission": emission_value})

        for month, emissions in monthly_emissions.items():
            for emission in emissions:
                emission_record = MonthlyUserEmissions(
                    userId=user_id,
                    date=datetime.strptime(month, '%Y-%m'),
                    category=emission["category"],
                    emission=emission["emission"]
                )
                db.session.add(emission_record)

        db.session.commit()

    emissions_data = {
        month: emissions
        for month, emissions in monthly_emissions.items()
    }

    return jsonify(emissions_data), 200

model = joblib.load('models/offset_recommendation_model.pkl')
user_project_matrix = joblib.load('models/user_project_matrix.pkl')

@main.route('/recommend-offset', methods=['GET'])
@jwt_required()
def recommend_offset():
    user_id = get_jwt_identity()
    current_month = datetime.now().strftime('%Y-%m')

    # Check if there's already a recommendation for the current month
    existing_recommendation = MonthlyRecommendations.query.filter_by(userId=user_id, date=datetime.strptime(current_month, '%Y-%m')).first()
    
    if existing_recommendation:
        return jsonify({"msg": "You have already chosen an offset project for this month."}), 409
    
    try:
        user_index = user_project_matrix.index.get_loc(user_id)
    except KeyError:
        return jsonify({"msg": "User not found in the recommendation matrix."}), 404

    distances, indices = model.kneighbors(user_project_matrix.iloc[user_index, :].values.reshape(1, -1), n_neighbors=2)
    
    if len(indices[0]) < 2:
        return jsonify({"msg": "Not enough similar users found for recommendations."}), 404

    similar_user_index = indices[0][1]
    similar_user_id = user_project_matrix.index[similar_user_index]

    recommendations = MonthlyRecommendations.query.filter_by(userId=similar_user_id).all()
    if not recommendations:
        return jsonify({"msg": "No recommendations found."}), 404

    recommended_project = recommendations[0]  # Take the first recommendation for simplicity
    project_details = ProjectDetails.query.filter_by(projectName=recommended_project.project).first()

    if not project_details:
        return jsonify({"msg": "Project details not found."}), 404

    return jsonify({
        "userId": user_id,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "project": project_details.projectName,
        "category": project_details.category,
        "description": project_details.description
    }), 200

@main.route('/save-recommendation', methods=['POST'])
@jwt_required()
def save_recommendation():
    user_id = get_jwt_identity()
    data = request.json

    current_date = datetime.now().strftime('%Y-%m-%d')

    # Check if there's already a recommendation for the current month
    existing_recommendation = MonthlyRecommendations.query.filter_by(userId=user_id, date=datetime.strptime(current_date, '%Y-%m-%d')).first()
    
    if existing_recommendation:
        return jsonify({"msg": "You have already chosen an offset project for this month."}), 409

    recommendation = MonthlyRecommendations(
        userId=user_id,
        date=datetime.strptime(current_date, '%Y-%m-%d'),
        project=data['project'],
        category=data['category'],
        description=data['description'],
        rating=None 
    )
    db.session.add(recommendation)
    db.session.commit()

    return jsonify({"msg": "Recommendation saved."}), 200

@main.route('/rate-recommendation', methods=['POST'])
@jwt_required()
def rate_recommendation():
    user_id = get_jwt_identity()
    data = request.json

    recommendation = MonthlyRecommendations.query.filter_by(userId=user_id, date=datetime.strptime(data['date'], '%Y-%m-%d')).first()
    if recommendation:
        recommendation.rating = data['rating']
        db.session.commit()
        return jsonify({"msg": "Recommendation rated."}), 200

    return jsonify({"msg": "Recommendation not found."}), 404

@main.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()
    recommendations = MonthlyRecommendations.query.filter_by(userId=user_id).all()
    recommendation_list = [
        {
            "date": recommendation.date,
            "project": recommendation.project,
            "category": recommendation.category,
            "description": recommendation.description,
            "rating": recommendation.rating,
        }
        for recommendation in recommendations
    ]
    return jsonify(recommendation_list), 200

@main.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    transactions = Transactions.query.filter_by(userId=user_id).all()

    monthly_expenses = {}
    for transaction in transactions:
        month = transaction.date.strftime('%Y-%m')
        if month not in monthly_expenses:
            monthly_expenses[month] = {}
        if transaction.category not in monthly_expenses[month]:
            monthly_expenses[month][transaction.category] = 0
        monthly_expenses[month][transaction.category] += transaction.amount

    return jsonify(monthly_expenses), 200

@main.route('/emissions', methods=['GET'])
@jwt_required()
def get_emissions():
    user_id = get_jwt_identity()

    emissions = MonthlyUserEmissions.query.filter_by(userId=user_id).all()
    emission_data = {}
    for emission in emissions:
        month = emission.date.strftime('%Y-%m')
        if month not in emission_data:
            emission_data[month] = []
        emission_data[month].append({"category": emission.category, "emission": emission.emission})

    return jsonify(emission_data), 200





