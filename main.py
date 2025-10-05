from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Optional
from mangum import Mangum  # <-- for serverless

# Load CSV
students = []
with open('q-fastapi.csv.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students.append({"studentId": int(row["studentId"]), "class": row["class"]})

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# API endpoint
@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    if class_:
        filtered_students = [s for s in students if s["class"] in class_]
    else:
        filtered_students = students
    return {"students": filtered_students}

# Adapt for serverless
handler = Mangum(app)
