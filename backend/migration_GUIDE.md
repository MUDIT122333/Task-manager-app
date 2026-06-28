# SQLite → PostgreSQL Migration Guide
### Task Manager App (Flask + Windows)

---

## What We Did & What You Need to Do Next

---

## COMPLETED ✅

### 1. PostgreSQL 18 Installed
- Installed at `C:\Program Files\PostgreSQL\18\`
- Superuser: `postgres` / Password: `admin123`
- PATH added: `C:\Program Files\PostgreSQL\18\bin`

### 2. Database & User Created
```sql
CREATE DATABASE taskmanager_db;
CREATE USER taskmanager_user WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE taskmanager_db TO taskmanager_user;
GRANT ALL ON SCHEMA public TO taskmanager_user;
ALTER DATABASE taskmanager_db OWNER TO taskmanager_user;
```

### 3. Data Migrated
- Ran `migrate.py` — Users, Projects, Tasks moved to PostgreSQL
- SQLite backup saved at `backend/instance/taskmanager.db.backup`

### 4. Flask App Updated
- `app.py` now reads `DATABASE_URL` from `.env`
- `psycopg2-binary` and `python-dotenv` added to `requirements.txt`
- App tested and running successfully on PostgreSQL

### 5. Git Branch Created
- Branch: `postgres-migration`

---

## TO DO ⏳

### Step 1 — Commit & push your branch
```powershell
cd "C:\Users\mudit\OneDrive\Task-management\Task-manager-app"
git add .
git commit -m "feat: migrate database from SQLite to PostgreSQL"
git push origin feature/postgresql-migration
```

### Step 2 — Add .env to .gitignore
Make sure your `.gitignore` has this line so secrets are never pushed:
```
.env
```
Check it:
```powershell
cat .gitignore
```

### Step 3 — Create .env.example for teammates
Create `backend/.env.example` (safe to commit):
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/taskmanager_db
JWT_SECRET_KEY=your-secret-key
```

### Step 4 — Test all API endpoints
Start your server and test every route:
```powershell
cd backend
venv\Scripts\activate
python app.py
```
Test these endpoints:
- `POST /api/auth/signup` — register a new user
- `POST /api/auth/login` — login
- `GET  /api/projects` — list projects
- `POST /api/projects` — create a project
- `GET  /api/tasks` — list tasks
- `POST /api/tasks` — create a task

### Step 5 — Merge to main (after testing)
```powershell
git checkout main
git merge feature/postgresql-migration
git push origin main
```

### Step 6 — Deploy to production (choose one)
| Platform   | Command / Steps |
|------------|----------------|
| Supabase   | Create project at supabase.com → copy DATABASE_URL → update .env |
| Railway    | Connect GitHub repo → add DATABASE_URL env var → deploy |
| Render     | New Web Service → add PostgreSQL addon → set DATABASE_URL |
| AWS RDS    | Create PostgreSQL instance → update DATABASE_URL in .env |

For any cloud platform, update your `.env` with the production `DATABASE_URL`:
```
DATABASE_URL=postgresql://user:password@cloud-host:5432/dbname
```

---

## File Changes Summary

| File | Change |
|------|--------|
| `backend/app.py` | Replaced SQLite URI with `os.environ.get('DATABASE_URL')` |
| `backend/.env` | Added `DATABASE_URL` and `JWT_SECRET_KEY` (never commit!) |
| `backend/requirements.txt` | Added `psycopg2-binary`, `python-dotenv` |
| `backend/migrate.py` | Migration script (can delete after migration) |
| `backend/instance/taskmanager.db.backup` | SQLite backup (keep for 30 days) |

---

## Useful Commands

```powershell
# Start PostgreSQL (if stopped)
net start postgresql-x64-18

# Connect to your database
psql -U postgres -d taskmanager_db

# Check your tables
psql -U postgres -d taskmanager_db -c "\dt"

# Check row counts
psql -U postgres -d taskmanager_db -c "SELECT COUNT(*) FROM \"user\";"
psql -U postgres -d taskmanager_db -c "SELECT COUNT(*) FROM project;"
psql -U postgres -d taskmanager_db -c "SELECT COUNT(*) FROM task;"

# Activate venv
venv\Scripts\activate

# Run app
python app.py
```

---

## Important Notes
- Never commit `.env` to Git — it contains your passwords
- Keep `taskmanager.db.backup` for at least 30 days
- Use `taskmanager_user` (not `postgres`) for your app connection
- On production, always use a strong random `JWT_SECRET_KEY`
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---
*Migration completed on 28 June 2026*
