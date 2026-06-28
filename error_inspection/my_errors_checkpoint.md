# Local Setup Checkpoint — Task Manager App

## Stack
- **Frontend:** React (localhost:3000)
- **Backend:** Flask + SQLite (localhost:5000)

---

## Errors Encountered & Fixes

### 1. `pip` not found / venv issues
**Error:** `No module named pip`
**Fix:**
```bash
C:\Users\mudit\AppData\Local\Programs\Python\Python312\python.exe -m ensurepip --upgrade

# Then create venv using full Python path:
C:\Users\mudit\AppData\Local\Programs\Python\Python312\python.exe -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 2. Frontend hitting production URL instead of localhost
**Error:** Login returning 400 from Render (production backend)
**Root cause:** `Login.js` had hardcoded production URL:
```js
fetch('https://task-manager-backend-l0h5.onrender.com/api/auth/login')
```
**Fix:** Use environment variable instead:
```js
fetch(`${process.env.REACT_APP_API_URL}/api/auth/login`)
```
Create `frontend/.env` for local:
```
REACT_APP_API_URL=http://localhost:5000
```
Create `frontend/.env.production` for production:
```
REACT_APP_API_URL=https://task-manager-backend-l0h5.onrender.com
```
> Always restart `npm start` after changing `.env` files.

---

### 3. Login returning 404
**Error:** `/api/auth/login` not found
**Root cause:** Database tables not created — `db.create_all()` was commented out in `app.py`
**Fix:** Run once in Python shell:
```python
from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print('Tables created!')
```

---

### 4. Login returning 401 — Invalid username or password
**Error:** User doesn't exist in local database (local DB starts empty)
**Fix:** Create user manually in Python shell:
```bash
cd backend
venv\Scripts\activate
python
```
```python
from app import app
from extensions import db
from models import User

with app.app_context():
    db.create_all()
    user = User(username='mudit', email='mudit@gmail.com', role='member')
    user.set_password('your_password')
    db.session.add(user)
    db.session.commit()
    print('User created!')
```
Verify user exists:
```python
with app.app_context():
    users = User.query.all()
    for u in users:
        print(u.id, u.username, u.email)
```

---

### 5. Login returning `net::ERR_` / Network error
**Error:** Flask server crashed mid-session
**Fix:** Restart Flask:
```bash
python app.py
```
Make sure you see:
```
* Running on http://127.0.0.1:5000
```

---

## How to Run Locally (Every Time)

**Terminal 1 — Backend:**
```bash
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm start
```

---

## Key Reminders
- Local DB (`instance/taskmanager.db`) is separate from production — always create a user locally first
- Never hardcode production URLs in frontend code — use `.env` files
- Restart `npm start` after any `.env` change
- Run `db.create_all()` once whenever setting up on a new machine
