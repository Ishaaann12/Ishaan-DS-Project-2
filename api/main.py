import sys
import os

# ✅ Add the root directory (Project-2/) to Python's import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tasks.tasks import handle_task  # ✅ Ensure this import works
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tasks import handle_task  # Import dynamic task handler
from typing import Optional
from utils.file_process import handle_file_processing  # Import file processing utility
from tasks.tasks import handle_task # Import HTTP GET request handler
import tasks
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)  # Ensure file is optional
):
    if file:
        print(f"📂 Received file: {file.filename}")
    else:
        print("📂 No file uploaded.")
    answer = handle_task(question, file)
    return JSONResponse(content={"answer": answer})  # Ensure proper JSON output


@app.post("/run")
async def run_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)  
):
    print(f"📩 Received POST request with question: {question}")  # Debugging

    # Directly call `handle_task` (removed unnecessary `handle_file_processing`)
    answer = handle_task(question, file)

    return JSONResponse(content={"answer": answer})





@app.get("/api/health")
def health_check():
    return {"status": "OK"}


@app.get("/docs")
def docs_redirect():
    return {"message": "Swagger UI should be at /docs"}