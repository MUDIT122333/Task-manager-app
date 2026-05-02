from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import User

class UsersResource(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        return {
            "users": [user.to_dict() for user in users]
        }, 200