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

def duration_to_string(duration):
    """Convert duration object to readable string"""
    if isinstance(duration, dict):
        value = duration.get("value", 0)
        unit = duration.get("unit", "days")
        return f"{value} {unit}"
    # Fallback for old data format
    return f"{duration} days"

def duration_to_hours(duration):
    """Convert any duration to hours for comparison"""
    if isinstance(duration, dict):
        value = duration.get("value", 0)
        unit = duration.get("unit", "days")
    else:
        value = duration
        unit = "days"
    
    conversion = {
        "minutes": value / 60,
        "hours": value,
        "days": value * 24,
        "weeks": value * 24 * 7,
        "months": value * 24 * 30
    }
    return conversion.get(unit, value * 24)
