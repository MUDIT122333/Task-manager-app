🚀 Team Task Manager

A full-stack task management web application built with Flask (backend) and React (frontend).

✨ Features
JWT Authentication (Signup/Login)
Role-based access (Admin / Member)
Project creation & management
Task assignment & tracking
Dashboard with stats
Responsive UI

🧰 Tech Stack
Backend: Flask, Flask-RESTful, Flask-JWT-Extended
Database: SQLite (Render persistent disk recommended ⚠️)
Frontend: React
Deployment:
Backend → Render
Frontend → Vercel

📁 Project Structure
team-task-manager/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   └── tasks.py
│   ├── requirements.txt
│   └── database.db
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── .env.production
⚙️ Local Setup
🔹 Backend
cd backend
pip install -r requirements.txt
python app.py

Runs at:

http://localhost:5000
🔹 Frontend
cd frontend
npm install
npm start

Runs at:

http://localhost:3000
🌐 Deployment Guide
🔥 Backend Deployment (Render)
✅ Step 1: Push to GitHub

Make sure your backend is inside:

/backend
✅ Step 2: Create Render Web Service
Go to 👉 https://render.com
Click New → Web Service
Connect your GitHub repo
✅ Step 3: Configure
Setting	Value
Root Directory	backend
Runtime	Python
Build Command	pip install -r requirements.txt
Start Command	python app.py
✅ Step 4: Add Environment Variables

In Render → Environment:

JWT_SECRET_KEY=your_secret_key_here
⚠️ IMPORTANT (VERY COMMON ISSUE)

Update your app.py:

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
✅ After Deploy

You will get:

https://your-backend.onrender.com
⚠️ Test API

Open in browser:

https://your-backend.onrender.com/api/auth/login

👉 If you see JSON error → backend is working ✅

⚡ Frontend Deployment (Vercel)
✅ Step 1: Go to Vercel

👉 https://vercel.com

Click:

New Project → Import GitHub Repo
✅ Step 2: Configure
Setting	Value
Framework	React
Root Directory	frontend
✅ Step 3: Environment Variable

VERY IMPORTANT:

Add:

REACT_APP_API_URL=https://your-backend.onrender.com
✅ Step 4: Deploy

Click Deploy

⚠️ Fix React Routing Issue (IMPORTANT)

Create file:

frontend/vercel.json

Add:

{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
🔗 Connect Frontend → Backend

In your React code (e.g., API calls):

const API_URL = process.env.REACT_APP_API_URL;

Example:

fetch(`${API_URL}/api/projects`)
🧪 Test the App
👤 Admin
Create project
Assign tasks
👥 Member
View tasks
Update status
⚠️ Common Issues (VERY IMPORTANT)
❌ 1. "Not Found" on Render

Cause: Wrong route
Fix: Use /api/...

❌ 2. CORS Error

Fix in backend:

from flask_cors import CORS
CORS(app)
❌ 3. JWT Error (YOU FACED THIS)

Fix:

create_access_token(identity=str(user.id))
❌ 4. Vercel Build Failed

Fix ESLint errors OR disable CI strict mode:

Create .env in frontend:

CI=false
❌ 5. Netlify/Vercel shows 404

Fix:

Add vercel.json
Use correct routes
❌ 6. Projects API returning 500

Cause: JWT subject issue
Fix: (already solved above)
