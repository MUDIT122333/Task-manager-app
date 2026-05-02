# Team Task Manager

A full-stack task management web application built with Flask (backend) and React (frontend).

## Features

- User authentication (signup/login) with JWT tokens
- Role-based access control (Admin vs Member)
- Project management
- Task creation and assignment
- Task status tracking (TODO, IN PROGRESS, DONE)
- Dashboard with statistics
- Modern responsive UI

## Tech Stack

- **Backend**: Python Flask, Flask-RESTful, Flask-JWT-Extended
- **Database**: SQLite
- **Frontend**: React, CSS3
- **Deployment**: Railway

## Project Structure

```
team-task-manager/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── api/
│   │   ├── auth.py         # Authentication APIs
│   │   ├── projects.py     # Project APIs
│   │   └── tasks.py        # Task APIs
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Railway deployment file
│   └── database.db        # SQLite database
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CreateTaskForm.js
│   │   │   ├── CreateProjectForm.js
│   │   │   └── TaskStatusUpdate.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   └── Dashboard.js
│   │   ├── App.js         # Main React app
│   │   └── App.css        # Styles
│   ├── package.json
│   └── .env.production    # Production environment variables
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask app:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React app:
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - User login

### Projects
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create new project (Admin only)
- `GET /api/projects/<id>` - Get specific project
- `PUT /api/projects/<id>` - Update project (Admin only)
- `DELETE /api/projects/<id>` - Delete project (Admin only)

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task (Admin only)
- `GET /api/tasks/<id>` - Get specific task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task (Admin only)

## User Roles

### Admin
- Create projects
- Create and assign tasks
- View all projects and tasks
- Delete projects and tasks

### Member
- View assigned tasks
- Update task status
- View projects they're assigned to

## Deployment on Railway

### Backend Deployment

1. Push code to GitHub
2. Create new Railway project
3. Connect to the `backend` folder
4. Set environment variables:
   - `PYTHON_VERSION`: `3.9`
5. Railway will automatically detect and deploy the Flask app

### Frontend Deployment

1. Create another Railway project
2. Connect to the `frontend` folder
3. Set environment variables:
   - `REACT_APP_API_URL`: Your backend Railway URL
4. Railway will build and deploy the React app

## Testing the App

1. Create an admin account:
   - Username: `admin`
   - Password: `admin123`
   - Role: `admin`

2. Create a member account:
   - Username: `member1`
   - Password: `member123`
   - Role: `member`

3. Login as admin to:
   - Create projects
   - Create and assign tasks

4. Login as member to:
   - View assigned tasks
   - Update task status

## Environment Variables

### Backend
- `JWT_SECRET_KEY`: Your JWT secret key
- `DATABASE_URL`: Railway database URL (automatically set)

### Frontend
- `REACT_APP_API_URL`: Backend API URL

## Common Issues

1. **CORS Issues**: Make sure backend has CORS enabled
2. **JWT Token**: Check token is being sent in Authorization header
3. **Database**: SQLite file should be in backend directory
4. **Port Conflicts**: Backend uses 5000, Frontend uses 3000
