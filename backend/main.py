from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from bson import ObjectId
from models import plans_collection, tasks_collection, plan_helper, task_helper
from fastapi.responses import StreamingResponse
import io
import csv
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

app = FastAPI(title="Smart Task Planner")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Smart Task Planner API with MongoDB!"}

@app.post("/api/plan")
async def create_plan(goal: str):
    """Generate a task plan and save it to MongoDB"""
    
    prompt = f"""
        Break down this goal into actionable tasks with dependencies.

        Goal: {goal}

        Provide a JSON response with this structure:
        {{
            "tasks": [
                {{
                    "id": 1,
                    "name": "task name",
                    "description": "detailed description of what to do",
                    "estimated_duration": {{
                        "value": 2,
                        "unit": "days"
                    }},
                    "priority": "High",
                    "dependencies": []
                }}
            ]
        }}

        Rules:
        - Create 5-8 tasks
        - Dependencies should be task IDs that must be completed first (empty array if no dependencies)
        - Priority can be: High, Medium, or Low
        - estimated_duration must have "value" (number) and "unit" (one of: minutes, hours, days, weeks, months)
        - Choose appropriate time units based on task complexity:
        * minutes: for very quick tasks (5-60 minutes)
        * hours: for tasks taking part of a day (1-23 hours)
        * days: for tasks taking full days (1-30 days)
        * weeks: for longer tasks (1-12 weeks)
        * months: for very long tasks (1-12 months)
        - Use realistic estimates for each task

        Return ONLY the JSON, no other text.
        """

    
    # Generate plan with AI
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    plan_data = json.loads(response.text)
    
    # Save plan to MongoDB
    plan = {"goal": goal}
    result = await plans_collection.insert_one(plan)
    plan_id = result.inserted_id
    
    # Save tasks with new duration format
    for task_data in plan_data["tasks"]:
        task = {
            "plan_id": plan_id,
            "task_number": task_data["id"],
            "name": task_data["name"],
            "description": task_data["description"],
            "estimated_duration": task_data["estimated_duration"],  # Now stores object
            "priority": task_data["priority"],
            "dependencies": task_data["dependencies"],
            "status": "pending"
        }
        await tasks_collection.insert_one(task)
    
    db.commit()
    
    return {
        "success": True,
        "plan_id": str(plan_id),
        "message": "Plan created and saved to MongoDB!",
        "plan": plan_data
    }

@app.get("/api/plans")
async def get_all_plans():
    """Get all saved plans"""
    plans = []
    async for plan in plans_collection.find():
        plan_id = plan["_id"]
        task_count = await tasks_collection.count_documents({"plan_id": plan_id})
        plans.append({
            "id": str(plan_id),
            "goal": plan["goal"],
            "task_count": task_count
        })
    
    return {"plans": plans}

@app.get("/api/plan/{plan_id}")
async def get_plan(plan_id: str):
    """Get a specific plan with all its tasks"""
    try:
        plan = await plans_collection.find_one({"_id": ObjectId(plan_id)})
    except:
        return {"error": "Invalid plan ID"}
    
    if not plan:
        return {"error": "Plan not found"}
    
    tasks = []
    async for task in tasks_collection.find({"plan_id": ObjectId(plan_id)}):
        tasks.append({
            "id": task["task_number"],
            "name": task["name"],
            "description": task["description"],
            "estimated_duration": task["estimated_duration"],  # Return as object
            "priority": task["priority"],
            "dependencies": task["dependencies"],
            "status": task.get("status", "pending")
        })
    
    # Calculate progress
    total = len(tasks)
    completed = len([t for t in tasks if t["status"] == "completed"])
    progress = (completed / total * 100) if total > 0 else 0
    
    return {
        "id": str(plan["_id"]),
        "goal": plan["goal"],
        "tasks": tasks,
        "progress": round(progress, 2)
    }


@app.patch("/api/task/{plan_id}/{task_number}/status")
async def update_task_status(plan_id: str, task_number: int, status: str):
    """Update task status"""
    valid_statuses = ["pending", "in_progress", "completed"]
    if status not in valid_statuses:
        return {"error": f"Invalid status. Must be one of: {valid_statuses}"}
    
    try:
        result = await tasks_collection.update_one(
            {"plan_id": ObjectId(plan_id), "task_number": task_number},
            {"$set": {"status": status}}
        )
    except:
        return {"error": "Invalid plan ID"}
    
    if result.modified_count == 0:
        return {"error": "Task not found"}
    
    return {
        "success": True,
        "message": f"Task status updated to '{status}'"
    }

@app.get("/api/plan/{plan_id}/progress")
async def get_plan_progress(plan_id: str):
    """Get progress statistics"""
    try:
        plan = await plans_collection.find_one({"_id": ObjectId(plan_id)})
    except:
        return {"error": "Invalid plan ID"}
    
    if not plan:
        return {"error": "Plan not found"}
    
    all_tasks = []
    async for task in tasks_collection.find({"plan_id": ObjectId(plan_id)}):
        all_tasks.append(task)
    
    total_tasks = len(all_tasks)
    completed = len([t for t in all_tasks if t.get("status") == "completed"])
    in_progress = len([t for t in all_tasks if t.get("status") == "in_progress"])
    pending = len([t for t in all_tasks if t.get("status") == "pending"])
    
    progress_percentage = (completed / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "plan_id": str(plan["_id"]),
        "goal": plan["goal"],
        "total_tasks": total_tasks,
        "completed": completed,
        "in_progress": in_progress,
        "pending": pending,
        "progress_percentage": round(progress_percentage, 2)
    }

@app.delete("/api/plan/{plan_id}")
async def delete_plan(plan_id: str):
    """Delete a plan and all its tasks"""
    try:
        await tasks_collection.delete_many({"plan_id": ObjectId(plan_id)})
        result = await plans_collection.delete_one({"_id": ObjectId(plan_id)})
    except:
        return {"error": "Invalid plan ID"}
    
    if result.deleted_count == 0:
        return {"error": "Plan not found"}
    
    return {"success": True, "message": "Plan deleted"}

@app.get("/api/plan/{plan_id}/export/csv")
async def export_plan_csv(plan_id: str):
    """Export plan as CSV file"""
    try:
        plan = await plans_collection.find_one({"_id": ObjectId(plan_id)})
    except:
        return {"error": "Invalid plan ID"}
    
    if not plan:
        return {"error": "Plan not found"}
    
    # Get all tasks
    tasks = []
    async for task in tasks_collection.find({"plan_id": ObjectId(plan_id)}):
        duration = task["estimated_duration"]
        if isinstance(duration, dict):
            duration_str = f"{duration['value']} {duration['unit']}"
        else:
            duration_str = f"{duration} days"
            
        tasks.append({
            "Task ID": task["task_number"],
            "Task Name": task["name"],
            "Description": task["description"],
            "Estimated Duration": duration_str,
            "Priority": task["priority"],
            "Dependencies": ", ".join(map(str, task["dependencies"])) if task["dependencies"] else "None",
            "Status": task.get("status", "pending")
        })
    
    if not tasks:
        return {"error": "No tasks found"}
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=tasks[0].keys())
    
    # Write header and rows
    writer.writeheader()
    writer.writerows(tasks)
    
    # Prepare response
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=task_plan_{plan_id}.csv"
        }
    )

