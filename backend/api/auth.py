from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from sqlalchemy import or_

class SignupResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data or not data.get('username') or not data.get('email') or not data.get('password'):
                return {'error': 'Username and password are required'}, 400
            
            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 400
            
            if User.query.filter_by(email=data['email']).first():
                return {'error' : 'Email already exists'}, 400
            
            # Create new user
            user = User(
                username=data['username'],
                email=data['email'],
                role='member'  # Default to member
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(identity=str(user.id))
            
            return {
                'message': 'User created successfully',
                'user': user.to_dict(),
                'access_token': access_token
            }, 201
            
        except Exception as e:
            db.session.rollback()
            print("ERROR:", e)   # 👈 VERY IMPORTANT
            return {'error': str(e)}, 500

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            print(data)
            
            # Validate required fields
            if not data or not data.get('identifier') or not data.get('password'):
                return {'error': 'identifier and password are required'}, 400
            
            # Find user
            identifier = data.get("identifier")
            user = User.query.filter(or_(User.username == identifier,
                                            User.email == identifier)).first()
            
            # Check credentials
            if not user or not user.check_password(data['password']):
                return {'error': 'Invalid username or password'}, 401
            
            # Create access token
            access_token = create_access_token(identity=str(user.id))

            print("Received:", data)

            identifier = data.get("identifier")
            print("Identifier:", identifier)

            user = User.query.filter(
                or_(User.username == identifier, User.email == identifier)
            ).first()

            print("User:", user)

            if user:
                print("Password Match:", user.check_password(data["password"]))
            
            return {
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token
            }, 200
            
        except Exception as e:
            return {'error': 'Login failed'}, 500
