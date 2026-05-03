from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Project, Task
from datetime import datetime

class TasksResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            
            # Get query parameters
            project_id = request.args.get('project_id')
            status = request.args.get('status')
            
            # Build query
            query = Task.query
            
            if user.role != 'admin':
                # Members can only see their assigned tasks
                query = query.filter_by(assigned_to=user_id)
            
            if project_id:
                query = query.filter_by(project_id=project_id)
            
            if status:
                query = query.filter_by(status=status)
            
            tasks = query.all()
            
            return {
                'tasks': [task.to_dict() for task in tasks]
            }, 200
            
        except Exception as e:
            return {'error': 'Failed to fetch tasks'}, 500
    
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            # Only admin can create tasks
            if user.role != 'admin':
                return {'error': 'Only admin can create tasks'}, 403
            
            data = request.get_json()
            
            # Validate required fields
            if not data or not data.get('title') or not data.get('project_id'):
                return {'error': 'Title and project_id are required'}, 400
            
            # Check if project exists
            project = Project.query.get(data['project_id'])
            if not project:
                return {'error': 'Project not found'}, 404
            
            # Parse deadline if provided
            deadline = None
            if data.get('deadline'):
                try:
                    deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
                except:
                    return {'error': 'Invalid deadline format. Use ISO format.'}, 400
            
            task = Task(
                title=data['title'],
                description=data.get('description', ''),
                status=data.get('status', 'TODO'),
                priority=data.get('priority', 'MEDIUM'),
                assigned_to=data.get('assigned_to'),
                project_id=data['project_id'],
                deadline=deadline
            )
            
            db.session.add(task)
            db.session.commit()
            
            return {
                'message': 'Task created successfully',
                'task': task.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create task'}, 500

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            task = Task.query.get_or_404(task_id)
            
            # Check access permissions
            if user.role != 'admin' and task.assigned_to != user_id:
                return {'error': 'Access denied'}, 403
            
            return {
                'task': task.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': 'Failed to fetch task'}, 500
    
    @jwt_required()
    def put(self, task_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            task = Task.query.get_or_404(task_id)
            
            # Check access permissions
            if user.role != 'admin' and task.assigned_to != user_id:
                return {'error': 'Access denied'}, 403
            
            data = request.get_json()
            
            # Update fields
            if data.get('title'):
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if data.get('status'):
                task.status = data['status']
            if data.get('priority'):
                task.priority = data['priority']
            
            # Only admin can change assignment and project
            if user.role == 'admin':
                if 'assigned_to' in data:
                    task.assigned_to = data['assigned_to']
                if data.get('project_id'):
                    task.project_id = data['project_id']
            
            if data.get('deadline'):
                try:
                    task.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
                except:
                    return {'error': 'Invalid deadline format. Use ISO format.'}, 400
            
            task.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                'message': 'Task updated successfully',
                'task': task.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update task'}, 500
    
    @jwt_required()
    def delete(self, task_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            task = Task.query.get_or_404(task_id)
            
            # Only admin can delete tasks
            if user.role != 'admin':
                return {'error': 'Only admin can delete tasks'}, 403
            
            db.session.delete(task)
            db.session.commit()
            
            return {'message': 'Task deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete task'}, 500
