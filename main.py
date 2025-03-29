# from fastapi import FastAPI, Form, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import uvicorn
# from tasks import handle_http_get_request

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
#  )

# @app.post("/api/")
# async def answer_question(
#     question: str = Form(...), 
#     file: UploadFile = File(None)
# ):
#     if question.startswith("http"):
#         # Handle HTTP GET request questions
#         return handle_http_get_request(question)

#     if file:
#         # Handle file-related questions
#         return {"answer": f"Received file: {file.filename} for question: {question}"}

#     # Default response
#     return {"answer": "Processing question..."}
#     """
#     API endpoint to process questions and optional file uploads.
#     """
#     if file:
#         return {"answer": f"Received file: {file.filename} for question: {question}"}
#     return {"answer": f"Processing question: {question}"}

#    # Use task handler to process the question
#     result = tasks.task_handler(question)
#     return {"answer": result}
# @app.post("/api/")
# async def answer_question(
#     question: str = Form(...), 
#     file: UploadFile = File(None)
# ):
    # """
    # API endpoint to process questions and optional file uploads.
    # """
    # # Placeholder response (we'll implement logic later)
#     # return {"answer": "Processing logic goes here"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tasks import handle_task  # Import dynamic task handler
from typing import Optional
from utils import handle_file_processing  # Import file processing utility
from tasks import handle_http_get  # Import HTTP GET request handler
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

























# @app.post("/run")
# async def run_task(
#     question: str = Form(...), 
#     file: Optional[UploadFile] = File(None)  # Ensure file is optional
# ):
#     # Ensure the question is processed correctly
#     question_with_file = handle_file_processing(question, file)

#     # Check if the question (or modified version) exists in task mapping
#     if question_with_file in handle_task:
#         return handle_task[question_with_file](question_with_file, file)

#     return JSONResponse(content={"error": "Question not recognized."})
