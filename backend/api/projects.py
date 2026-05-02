from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Project, Task
from datetime import datetime

class ProjectsResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            
            # Admin can see all projects, members can see projects they're assigned to
            if user.role == 'admin':
                projects = Project.query.all()
            else:
                # Members see projects where they have assigned tasks
                projects = Project.query.join(Task).filter(Task.assigned_to == user_id).distinct().all()
            
            return {
                'projects': [project.to_dict() for project in projects]
            }, 200
            
        except Exception as e:
            db.session.rollback()
            print("PROJECT ERROR:", e)
            return {'error': str(e)}, 500
    
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            # Only admin can create projects
            if user.role != 'admin':
                return {'error': 'Only admin can create projects'}, 403
            
            data = request.get_json()
            
            if not data or not data.get('name'):
                return {'error': 'Project name is required'}, 400
            
            project = Project(
                name=data['name'],
                description=data.get('description', ''),
                created_by=user_id
            )
            
            db.session.add(project)
            db.session.commit()
            
            return {
                'message': 'Project created successfully',
                'project': project.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create project'}, 500

class ProjectResource(Resource):
    @jwt_required()
    def get(self, project_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            project = Project.query.get_or_404(project_id)
            
            # Check access permissions
            if user.role != 'admin':
                # Members can only see projects they're assigned to
                has_access = Task.query.filter_by(project_id=project_id, assigned_to=user_id).first()
                if not has_access:
                    return {'error': 'Access denied'}, 403
            
            return {
                'project': project.to_dict(),
                'tasks': [task.to_dict() for task in project.tasks]
            }, 200
            
        except Exception as e:
            return {'error': 'Failed to fetch project'}, 500
    
    @jwt_required()
    def put(self, project_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            project = Project.query.get_or_404(project_id)
            
            # Only admin can update projects
            if user.role != 'admin':
                return {'error': 'Only admin can update projects'}, 403
            
            data = request.get_json()
            
            if data.get('name'):
                project.name = data['name']
            if 'description' in data:
                project.description = data['description']
            
            db.session.commit()
            
            return {
                'message': 'Project updated successfully',
                'project': project.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update project'}, 500
    
    @jwt_required()
    def delete(self, project_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            project = Project.query.get_or_404(project_id)
            
            # Only admin can delete projects
            if user.role != 'admin':
                return {'error': 'Only admin can delete projects'}, 403
            
            db.session.delete(project)
            db.session.commit()
            
            return {'message': 'Project deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete project'}, 500
