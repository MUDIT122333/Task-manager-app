from flask import Flask
from extensions import db, jwt, cors
from flask_restful import Api
from datetime import timedelta

# 🔥 Import resources
from api.users import UsersResource
from api.auth import SignupResource, LoginResource
from api.projects import ProjectResource, ProjectsResource
from api.tasks import TaskResource, TasksResource

# 🔥 Import models
from models import User, Project, Task

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Init extensions
db.init_app(app)
jwt.init_app(app)
cors.init_app(app)
api = Api(app)

# 🔥 Create tables
with app.app_context():
    db.create_all()

# 🔥 Register ALL routes together
api.add_resource(UsersResource, '/api/users')
api.add_resource(SignupResource, '/api/auth/signup')
api.add_resource(LoginResource, '/api/auth/login')
api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
api.add_resource(ProjectsResource, '/api/projects')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
api.add_resource(TasksResource, '/api/tasks')

if __name__ == '__main__':
    app.run(debug=True, port=5000)