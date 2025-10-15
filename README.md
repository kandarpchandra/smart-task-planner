# 🎯 Smart Task Planner

AI-powered task planning system that breaks down goals into actionable tasks with timelines and dependencies using Google Gemini.

## Features

- ✅ AI-powered task decomposition
- ✅ Task dependency tracking
- ✅ Progress monitoring
- ✅ Priority-based task organization
- ✅ CSV export functionality
- ✅ MongoDB cloud database
- ✅ Responsive web interface

## Tech Stack

**Backend:**

- FastAPI
- Google Gemini 2.0 Flash (Free API)
- MongoDB Atlas (Free tier)
- Python 3.11+

**Frontend:**

- React (Vite)
- Axios
- Modern CSS

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- MongoDB Atlas account (free)
- Google Gemini API key (free)

### Backend Setup

1. Navigate to backend folder:
   cd backend

2. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate # Windows
   source venv/bin/activate # Mac/Linux

3. Install dependencies:
   pip install -r requirements.txt

4. Create `.env` file:
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URL=your_mongodb_connection_string_here

5. Run the server:
   python -m uvicorn main:app --reload

Backend will run at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend folder:
   cd frontend

2. Install dependencies:
   npm install

3. Run development server:
   npm run dev

Frontend will run at: `http://localhost:5173`

## API Endpoints

- `POST /api/plan` - Create new task plan
- `GET /api/plans` - Get all plans
- `GET /api/plan/{id}` - Get specific plan
- `PATCH /api/task/{plan_id}/{task_number}/status` - Update task status
- `GET /api/plan/{id}/progress` - Get plan progress
- `GET /api/plan/{id}/export/csv` - Export plan as CSV
- `DELETE /api/plan/{id}` - Delete plan

## Project Structure

smart-task-planner/
├── backend/
│ ├── main.py # FastAPI application
│ ├── models.py # MongoDB models
│ ├── requirements.txt # Python dependencies
│ └── .env # Environment variables
├── frontend/
│ ├── src/
│ │ ├── App.jsx # Main React component
│ │ └── App.css # Styling
│ └── package.json # Node dependencies
└── README.md
