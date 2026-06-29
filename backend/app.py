from flask import Flask
from extensions import db, jwt
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

#  Import resources
from api.health import HealthResource
from api.users import UsersResource
from api.auth import SignupResource, LoginResource
from api.projects import ProjectResource, ProjectsResource
from api.tasks import TaskResource, TasksResource

#  Import models
from models import User, Project, Task

app = Flask(__name__)

# Database — reads from .env file
# Tells SQLAlchemy WHICH database to connect to
# Value comes from .env — now points to Supabase PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Just turns off a noisy warning — nothing to do with DB type
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT secret key for token signing — nothing to do with database at all
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')


db.init_app(app)
jwt.init_app(app)

CORS(app)

api = Api(app)

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
