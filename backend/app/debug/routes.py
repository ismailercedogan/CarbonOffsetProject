from . import debug
from flask import jsonify
from app.models import Users


@debug.route('users', methods=['GET'])
def list_users():
    users = Users.query.all()
    user_list = []
    for user in users:
        user_info = {
            "userId": user.userId,
            "email": user.email,
            "passwordHash": user.passwordHash
        }
        user_list.append(user_info)
    return jsonify(user_list), 200
