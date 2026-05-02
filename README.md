# 🚀 Team Task Manager

A full-stack task management web application built with **Flask (backend)** and **React (frontend)**.

---

## ✨ Features

* JWT Authentication (Signup/Login)
* Role-based access (Admin / Member)
* Project creation & management
* Task assignment & tracking
* Dashboard with statistics
* Responsive UI

---

## 🧰 Tech Stack

* **Backend**: Flask, Flask-RESTful, Flask-JWT-Extended
* **Database**: SQLite (⚠️ use persistent disk on Render)
* **Frontend**: React
* **Deployment**:

  * Backend → Render
  * Frontend → Vercel

---

## 📁 Project Structure

```
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
```

---

## ⚙️ Local Setup

### 🔹 Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs at:
http://localhost:5000

---

### 🔹 Frontend

```bash
cd frontend
npm install
npm start
```

Runs at:
http://localhost:3000

---

## 🌐 Deployment Guide

---

## 🔥 Backend Deployment (Render)

### Step 1: Push to GitHub

Ensure backend is inside:

```
/backend
```

---

### Step 2: Create Render Service

* Go to https://render.com
* Click **New → Web Service**
* Connect GitHub repo

---

### Step 3: Configure

* Root Directory: `backend`
* Runtime: Python
* Build Command:

```bash
pip install -r requirements.txt
```

* Start Command:

```bash
python app.py
```

---

### Step 4: Environment Variables

```
JWT_SECRET_KEY=your_secret_key_here
```

---

### ⚠️ Important Fix

In `app.py`:

```python
import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

---

### Backend URL

```
https://your-backend.onrender.com
```

---

## ⚡ Frontend Deployment (Vercel)

### Step 1

Go to https://vercel.com
→ Import GitHub repo

---

### Step 2

* Framework: React
* Root Directory: `frontend`

---

### Step 3: Environment Variable

```
REACT_APP_API_URL=https://your-backend.onrender.com
```

---

### Step 4

Click **Deploy**

---

## ⚠️ Fix React Routing

Create:

```
frontend/vercel.json
```

Add:

```json
{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 🔗 API Connection

```javascript
const API_URL = process.env.REACT_APP_API_URL;

fetch(`${API_URL}/api/projects`);
```

---

## 🧪 Testing

### 👤 Admin

* Create projects
* Assign tasks

### 👥 Member

* View tasks
* Update status

---

## ⚠️ Common Issues

### ❌ 1. Render "Not Found"

Use correct route:

```
/api/...
```

---

### ❌ 2. CORS Error

```python
from flask_cors import CORS
CORS(app)
```

---

### ❌ 3. JWT Error

```python
create_access_token(identity=str(user.id))
```

---

### ❌ 4. Vercel Build Failed

Create `.env`:

```
CI=false
```

---

### ❌ 5. 404 on Vercel

Add `vercel.json`

---

### ❌ 6. API 500 Error

Cause:
JWT subject not string

Fix:

```
identity=str(user.id)
```

---

## 🚀 Final URLs

* Backend → https://task-manager-backend-l0h5.onrender.com
* Frontend → https://task-manager-app-pu88.vercel.app/
