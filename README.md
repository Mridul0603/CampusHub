# CampusHub — Smart Student Productivity Platform

## Quick Start

### Option 1: Docker (recommended for the DB)
```bash
# Start PostgreSQL
docker-compose up db -d

# Run backend locally
cd backend
cp .env.example .env   # fill in your values
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run frontend locally
cd frontend
npm install
npm run dev
```

### Option 2: Full Docker
```bash
cp backend/.env.example backend/.env   # fill in values
docker-compose up --build
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

## Project Structure
See ARCHITECTURE.md for full details.

## Modules
- [x] Module 1: Authentication (JWT + bcrypt)
- [ ] Module 2: Smart Notice Board
- [ ] Module 3: Event Management
- [ ] Module 4: Classroom Booking
- [ ] Module 5: Student Marketplace
- [ ] Module 6: Placement Hub
- [ ] Module 7: GoalTrack
