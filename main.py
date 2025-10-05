from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Optional

# -------------------------------
# Step 1: Load CSV data
# -------------------------------
students = []

with open('q-fastapi.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

# -------------------------------
# Step 2: Create FastAPI app
# -------------------------------
app = FastAPI()

# -------------------------------
# Step 3: Enable CORS for all origins
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],   # Allow all headers
)

# -------------------------------
# Step 4: Create API endpoint
# -------------------------------
@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    """
    Returns all students or filters by class if query parameters are provided.
    Examples:
    - /api -> all students
    - /api?class=1A -> only students in 1A
    - /api?class=1A&class=1B -> students in 1A or 1B
    """
    if class_:
        filtered_students = [s for s in students if s["class"] in class_]
    else:
        filtered_students = students

    return {"students": filtered_students}

# -------------------------------
# Step 5: Run server using:
# uvicorn main:app --reload
# -------------------------------
