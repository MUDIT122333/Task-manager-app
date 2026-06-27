from flask import Flask
from extensions import db, jwt
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta

#  Import resources
from api.health import HealthResource
from api.users import UsersResource
from api.auth import SignupResource, LoginResource
from api.projects import ProjectResource, ProjectsResource
from api.tasks import TaskResource, TasksResource

#  Import models
from models import User, Project, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
jwt.init_app(app)


CORS(app)

api = Api(app)

# Import models and routes after app initialization
from api.auth import SignupResource, LoginResource
from api.projects import ProjectResource, ProjectsResource
from api.tasks import TaskResource, TasksResource
from api.users import UsersResource


# API Routes
api.add_resource(SignupResource, '/api/auth/signup')
api.add_resource(LoginResource, '/api/auth/login')
api.add_resource(UsersResource, '/api/users')
api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
api.add_resource(ProjectsResource, '/api/projects')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
api.add_resource(TasksResource, '/api/tasks')
api.add_resource(HealthResource, '/health')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return {'message ': "task manager api is running."}
    
if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))