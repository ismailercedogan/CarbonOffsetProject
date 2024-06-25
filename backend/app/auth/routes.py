from . import auth  
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Users
from flask_cors import cross_origin

@auth.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins='http://localhost:3000', supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        return '', 200  # Handle preflight request


    data = request.json
    email = data.get('email')
    password = data.get('password')
        
    user = Users.query.filter_by(email=email).first()
    
    if user and user.passwordHash == password:  # Simple comparison for demo purposes
        access_token = create_access_token(identity=user.userId)
        return jsonify(access_token=access_token), 200

    print("Invalid credentials")  
    return jsonify({"msg": "Invalid credentials"}), 401

