AI Powered Career Guidance System
==========================

# NCTB:  This project in progress, We are working on it. It's not properly builded yet.

This archive contains two folders:
- frontend/  : your React Vite frontend (original repo) with a new API client at `src/api/client.ts`
- backend/   : Flask backend scaffold (JWT, SQLite, file uploads, admin, scheduler)

Quick local run (backend):
  cd backend
  python -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
  python app.py

Quick local run (frontend):
  cd frontend
  npm install
  cp .env.development .env
  npm run dev

Deployment notes (Render):
- Backend: the backend contains a Dockerfile and Procfile suitable for Render web service.
- Frontend: deploy as a static site build (npm run build) or as a Node service; set `VITE_API_BASE_URL`
  to point to the backend URL in Render environment variables.
