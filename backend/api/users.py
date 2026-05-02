from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

class UsersResource(Resource):
    @jwt_required()
    def get(self):
        try:
            users = User.query.all()
            return {
                'users': [user.to_dict() for user in users]
            }, 200
            
        except Exception as e:
            print("ERROR:", e)
            return {'error': 'Failed to fetch users'}, 500