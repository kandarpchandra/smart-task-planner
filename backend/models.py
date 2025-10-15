import os
from dotenv import load_dotenv
import motor.motor_asyncio
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB setup
MONGODB_URL = os.getenv("MONGODB_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.taskplanner

# Collections
plans_collection = database.get_collection("plans")
tasks_collection = database.get_collection("tasks")

# Helper functions
def plan_helper(plan) -> dict:
    return {
        "id": str(plan["_id"]),
        "goal": plan["goal"],
    }

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "plan_id": str(task["plan_id"]),
        "task_number": task["task_number"],
        "name": task["name"],
        "description": task["description"],
        "estimated_days": task["estimated_days"],
        "priority": task["priority"],
        "dependencies": task["dependencies"],
        "status": task.get("status", "pending")
    }
