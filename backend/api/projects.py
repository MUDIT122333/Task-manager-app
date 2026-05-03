from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Project, Task


class ProjectsResource(Resource):

    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if not user:
                return {'error': 'User not found'}, 404

            # Admin → all projects
            if user.role == 'admin':
                projects = Project.query.all()
            else:
                # Member → only assigned projects
                projects = Project.query.join(Task).filter(
                    Task.assigned_to == user_id
                ).distinct().all()

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
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            # 🔴 Fix 1: user check
            if not user:
                return {'error': 'User not found'}, 404

            # 🔴 Fix 2: admin check
            if user.role != 'admin':
                return {'error': 'Only admin can create projects'}, 403

            data = request.get_json()

            # 🔴 Fix 3: validation
            if not data or not data.get('name'):
                return {'error': 'Project name is required'}, 400

            # 🔴 Fix 4: safe creation
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
            print("CREATE PROJECT ERROR:", e)   # 🔥 VERY IMPORTANT
            return {'error': str(e)}, 500


class ProjectResource(Resource):

    @jwt_required()
    def get(self, project_id):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if not user:
                return {'error': 'User not found'}, 404

            project = Project.query.get_or_404(project_id)

            # Member access check
            if user.role != 'admin':
                has_access = Task.query.filter_by(
                    project_id=project_id,
                    assigned_to=user_id
                ).first()

                if not has_access:
                    return {'error': 'Access denied'}, 403

            return {
                'project': project.to_dict(),
                'tasks': [task.to_dict() for task in project.tasks]
            }, 200

        except Exception as e:
            print("GET PROJECT ERROR:", e)
            return {'error': str(e)}, 500


    @jwt_required()
    def put(self, project_id):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if not user:
                return {'error': 'User not found'}, 404

            project = Project.query.get_or_404(project_id)

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
            print("UPDATE PROJECT ERROR:", e)
            return {'error': str(e)}, 500


    @jwt_required()
    def delete(self, project_id):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if not user:
                return {'error': 'User not found'}, 404

            project = Project.query.get_or_404(project_id)

            if user.role != 'admin':
                return {'error': 'Only admin can delete projects'}, 403

            db.session.delete(project)
            db.session.commit()

            return {'message': 'Project deleted successfully'}, 200

        except Exception as e:
            db.session.rollback()
            print("DELETE PROJECT ERROR:", e)
            return {'error': str(e)}, 500