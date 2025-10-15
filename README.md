# 🎯 Smart Task Planner

<div align="center">

[![Python][Python-badge]][Python-url]
[![React][React-badge]][React-url]
[![FastAPI][FastAPI-badge]][FastAPI-url]
[![MongoDB][MongoDB-badge]][MongoDB-url]
[![License: MIT][License-badge]][License-url]

</div>

> An AI-powered task planning system that intelligently breaks down your goals into actionable tasks, complete with timelines and dependencies, using the power of Google's Gemini AI.

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [🔌 API Endpoints](#-api-endpoints)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [📬 Contact](#-contact)

## 📖 About The Project

This project was built to simplify goal-setting and project management. Instead of manually creating long to-do lists, you can simply input a high-level goal (e.g., "Launch a new marketing campaign"), and the AI will generate a structured plan with individual tasks, estimated durations, and their dependencies.

It's designed to be a smart assistant that helps you organize, track, and execute your projects more efficiently.

![Project Screenshot](https://via.placeholder.com/800x400.png?text=Smart+Task+Planner+Screenshot)

---

## ✨ Features

-   ✅ **AI-Powered Task Decomposition**: Automatically breaks down large goals into smaller, manageable tasks.
-   🔗 **Task Dependency Tracking**: Visualizes the relationships and order between tasks.
-   📊 **Progress Monitoring**: Track the completion status of your overall plan and individual tasks.
-   ⭐ **Priority-Based Organization**: Intelligently organizes tasks based on their priority and dependencies.
-   📄 **CSV Export**: Easily export your task plans to a CSV file for offline use or reporting.
-   ☁️ **Cloud Database**: All plans are securely stored in a MongoDB Atlas cloud database.
-   📱 **Responsive Web Interface**: A clean and modern UI that works on any device.

---

## 🛠️ Tech Stack

This project is built with a modern, powerful stack:

<div align="center">

| Backend                               | Frontend                             | Database                               |
| ------------------------------------- | ------------------------------------ | -------------------------------------- |
| **Python 3.11+** | **React (Vite)** | **MongoDB Atlas** |
| **FastAPI** | **Axios** |                                        |
| **Google Gemini API** | **Modern CSS** |                                        |

</div>

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

Make sure you have the following installed on your system:
-   **Python** 3.11 or higher
-   **Node.js** 18 or higher
-   A free **MongoDB Atlas** account: [cloud.mongodb.com](https://cloud.mongodb.com/)
-   A free **Google Gemini API Key**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```sh
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Create the virtual environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the `backend` directory and add your credentials:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    MONGODB_URL=your_mongodb_connection_string_here
    ```

5.  **Run the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```sh
    cd ../frontend
    ```

2.  **Install the required npm packages:**
    ```sh
    npm install
    ```

3.  **Run the React development server:**
    ```sh
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173`.

---

## 🔌 API Endpoints

Here are the available API endpoints:

| Method  | Endpoint                                     | Description                        |
| :------ | :------------------------------------------- | :--------------------------------- |
| `POST`  | `/api/plan`                                  | Create a new task plan.            |
| `GET`   | `/api/plans`                                 | Get all existing plans.            |
| `GET`   | `/api/plan/{id}`                             | Get a specific plan by its ID.     |
| `PATCH` | `/api/task/{plan_id}/{task_number}/status`   | Update the status of a single task.|
| `GET`   | `/api/plan/{id}/progress`                    | Get the current progress of a plan.|
| `GET`   | `/api/plan/{id}/export/csv`                  | Export a plan as a CSV file.       |
| `DELETE`| `/api/plan/{id}`                             | Delete a plan by its ID.           |


---

## 📂 Project Structure

'''
smart-task-planner/
├── backend/
│   ├── main.py           # FastAPI application logic
│   ├── models.py         # Pydantic and Motor models
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   └── App.css       # Global styles
│   └── package.json      # Node.js dependencies
└── README.md
'''
