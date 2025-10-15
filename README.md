# 🎯 Smart Task Planner

<div align="center">

[![Python][Python-badge]][Python-url]
[![React][React-badge]][React-url]
[![FastAPI][FastAPI-badge]][FastAPI-url]
[![MongoDB][MongoDB-badge]][MongoDB-url]

[![Website Link](https://img.shields.io/badge/View_Demo-28a745?style=for-the-badge)](https://smart-task-planner-alpha.vercel.app/)
</div>

<div align="center">
  <p><i>
    An intelligent task planning system that leverages Google's Gemini AI to break down high-level goals into a structured, actionable plan with dependencies and timelines.
  </i></p>
</div>

<div align="center">
  <img src="./demo/demo.gif" alt="Smart Task Planner Demo" width="800"/>
</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
- [🤖 How It Works](#-how-it-works)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [🔌 API Endpoints](#-api-endpoints)
- [📂 Project Structure](#-project-structure)

---

## 📖 About The Project

The Smart Task Planner was built to bridge the gap between ambitious goals and concrete actions. Often, the hardest part of achieving a goal is knowing where to start. This application solves that problem by taking a simple goal description—like "Launch a new product in 2 weeks"—and using AI-powered reasoning to generate a complete project plan.

The core of the project is a **FastAPI backend** that communicates with the **Google Gemini API** to perform logical decomposition of the user's goal. The generated plan, including tasks, timelines, and their inter-dependencies, is then stored in a **MongoDB** database and beautifully rendered by a **React frontend**.

This project fulfills the following objectives:
-   Generation of actionable task breakdowns from a simple text input.
-   Logical estimation of timelines and identification of task dependencies.
-   A clean, user-friendly interface to submit goals and visualize plans.
-   A well-designed RESTful API to handle all logic.

---

## ✨ Key Features

-   **AI-Powered Task Decomposition**: Leverages Google Gemini for sophisticated reasoning to create comprehensive task lists.
-   **Logical Timeline Generation**: The AI suggests realistic deadlines and durations for each task.
-   **Dependency Mapping**: Automatically identifies which tasks need to be completed before others can begin.
-   **Interactive Web Interface**: A modern frontend built with React and Vite to submit goals and view plans in a clean, organized manner.
-   **Persistent Storage**: Securely stores all generated plans in a MongoDB Atlas database for future reference.
-   **RESTful API**: A robust backend built with FastAPI provides clear and efficient endpoints for managing plans.
-   **Data Export**: Functionality to export a complete task plan to a CSV file.

---

## 🤖 How It Works

The application follows a simple yet powerful workflow:

1.  **Goal Submission**: The user enters a high-level goal into the React frontend.
2.  **API Request**: The frontend sends the goal to the FastAPI backend.
3.  **AI Reasoning**: The backend constructs a detailed prompt for the Google Gemini API, instructing it to break down the goal. A sample prompt looks like this:
    > *"Break down this goal: '{user_goal}' into actionable tasks with suggested deadlines and dependencies. Provide the output as a structured list."*
4.  **Plan Generation**: Gemini processes the request and returns a structured breakdown of tasks.
5.  **Database Storage**: The backend parses the AI's response, validates the data, and stores the complete plan in the MongoDB database.
6.  **Frontend Display**: The structured plan is sent back to the React client, where it is displayed to the user in an intuitive format.

---

## 🛠️ Tech Stack

This project is built using a modern and scalable technology stack.

| Category      | Technology                                                                                                    |
|---------------|---------------------------------------------------------------------------------------------------------------|
| **Backend** | [**Python**](https://www.python.org/), [**FastAPI**](https://fastapi.tiangolo.com/)                              |
| **Frontend** | [**React**](https://reactjs.org/), [**Vite**](https://vitejs.dev/), [**Axios**](https://axios-http.com/)          |
| **Database** | [**MongoDB Atlas**](https://www.mongodb.com/cloud/atlas)                                                      |
| **AI Model** | [**Google Gemini**](https://deepmind.google/technologies/gemini/)                                               |

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have the following installed:
-   Python 3.11+
-   Node.js v18+ and npm
-   A free [MongoDB Atlas](https://cloud.mongodb.com/) account and your connection string.
-   A free [Google Gemini API Key](https://makersuite.google.com/app/apikey).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/kandarpchandra/smart-task-planner.git](https://github.com/kandarpchandra/smart-task-planner.git)
    cd smart-task-planner
    ```

2.  **Backend Setup:**
    ```sh
    # Navigate to the backend directory
    cd backend

    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Create a .env file and add your credentials
    # (You can copy .env.example to .env)
    echo "GEMINI_API_KEY='YOUR_GEMINI_API_KEY'" > .env
    echo "MONGODB_URL='YOUR_MONGODB_CONNECTION_STRING'" >> .env

    # Run the server
    uvicorn main:app --reload
    ```
    Your backend API will be available at `http://localhost:8000`.

3.  **Frontend Setup:**
    ```sh
    # Navigate to the frontend directory from the root
    cd frontend

    # Install dependencies
    npm install

    # Run the development server
    npm run dev
    ```
    Your frontend will be available at `http://localhost:5173`.

---

## 🔌 API Endpoints

The backend provides the following RESTful API endpoints:

| Method   | Endpoint                                   | Description                        |
|:---------|:-------------------------------------------|:-----------------------------------|
| `POST`   | `/api/plan`                                | Create a new task plan from a goal.  |
| `GET`    | `/api/plans`                               | Retrieve all existing plans.       |
| `GET`    | `/api/plan/{id}`                           | Get a specific plan by its ID.     |
| `PATCH`  | `/api/task/{plan_id}/{task_number}/status` | Update the status of a single task.|
| `GET`    | `/api/plan/{id}/progress`                  | Get the completion progress of a plan.|
| `GET`    | `/api/plan/{id}/export/csv`                | Export a plan as a CSV file.       |
| `DELETE` | `/api/plan/{id}`                           | Delete a plan by its ID.           |

---

## 📂 Project Structure

The repository is organized with a clear separation between the frontend and backend applications.

```
smart-task-planner/
├── backend/
│   ├── main.py           # FastAPI application logic and API endpoints
│   ├── models.py         # Pydantic data models for validation
│   └── requirements.txt  # Python package dependencies
├── frontend/
│   ├── src/              # React application source code
│   └── package.json      # Node.js package dependencies
├── demo/
│   └── demo.gif          # Animated demo for the README
├── .gitignore            # Specifies files for Git to ignore
├── LICENSE               # Project's MIT license
└── README.md             # You are here!
```

[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[React-badge]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[MongoDB-badge]: https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/
[License-badge]: https://img.shields.io/github/license/kandarpchandra/smart-task-planner?style=for-the-badge
[License-url]: https://github.com/kandarpchandra/smart-task-planner/blob/main/LICENSE
