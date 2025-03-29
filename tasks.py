
from typing import Optional
import requests
from fastapi import UploadFile
from urllib.parse import urlencode
import re
import json
from config import AIPROXY_TOKEN

import json
import inspect
import os
import requests
from typing import Optional
from dotenv import load_dotenv
from fastapi import UploadFile

# Load API token securely
load_dotenv()
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

# Function to get embeddings using AI Proxy
def get_embedding(text: str):
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
    data = {"model": "text-embedding-3-small", "input": text}
    response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", json=data, headers=headers)
    return response.json()["data"][0]["embedding"]


import inspect
from typing import Optional
import requests
import json
import inspect
from typing import Optional

import inspect
from typing import Optional

def handle_task(question: str, file: Optional[UploadFile] = None):
    TASK_MAPPING = {
        "https": handle_http_get,
        "google sheets": process_google_sheets_formula,
        "excel": process_excel_formula,
        "multi-cursors": process_text_to_json_multicursors,
        "bounding box": using_nominatim_api,
        "hacker news post": search_hn_latest,
        "including both groups": calculate_total_marks

    }

    task_groups = {
        "extract_csv_from_zip": {"zip", "csv", "answer column"},
        "count_days_in_range": {"date range", "how many"},
        "sort_json_array": {"sort", "json", "array"},
        "process_zip_for_symbol_sum": {"encodings", "UTF-8", "CP-1252"},
        "process_readme_task": {"sha256sum", "npx", " -y prettier"},
        "count_different_lines": {"zip", "same number of lines", "identical files"},
        "process_light_pixel_task": {"brightness", "number of pixels", "There is a mistake"},
        "fetch_wikipedia_outline" : {"URL", "API endpoint"},
        "search_hn_latest": {"Hacker News", "latest post", "topic", "points"},
        "count_successful_requests": {"successful", "GET requests", "for pages"},
        "top_ip_data_usage" : {"Across all requests", "bytes", "volume of downloads"},
    }

    task_descriptions = {  
        "sort_json_array": "Sort a JSON array of objects based on a specific field.",
        "extract_csv_from_zip": "Extract a CSV file from a ZIP archive.",
        "count_days_in_range": "Count how many times a specific weekday appears in a given date range.",
        "process_text_to_json_multicursors": "Download the text file and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}. What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?",
        "calculate_filtered_size": "Download the zip file and extract it. Use ls with options to list all files in the folder along with their date and file size. What's the total size of all files at least some bytes large and modified on or after the specified date?",
        "count_different_lines": "Download the zip file and extract it. It has nearly some identical files with the same number of lines. How many lines are different between the text files.",
        "get_weather_forecast": "What is the JSON weather forecast description for the city?",
        "using_nominatim_api" : "What is the minimum/maximum latitude/longitude of the bounding box of the city in the country on Nominatim API? Value of the minimum/maximum latitude/longitude",
        "search_hn_latest": "What is the link to the latest Hacker News post mentioning topic having at least some points?",
        "calculate_total_marks": "What is the total marks of the students who scored more/less marks than some number in some subject in groups (including both groups)?",
        "count_unique_students": "How many unique students are there in the file?",
        "count_successful_requests": "What is the number of successful GET requests for pages under language from some time until before some time on a day?",
        "top_ip_data_usage" : "Across all requests under language/ on some date, how many bytes did the top IP address (by volume of downloads) download?"
    }

    file_path = None
    if file:
        file_path = handle_file_processing(file)

    normalized_question = question.lower().replace("-", "")  # Normalize the question for all checks

    print(f"📩 Received question: {question}")

    # **1️⃣ Exact Match Check**
    for keyword, function in TASK_MAPPING.items():
        if keyword in normalized_question:
            print(f"✅ Exact match found: {keyword}, calling {function.__name__}")
            sig = inspect.signature(function)
            return function(question, file_path) if "file_path" in sig.parameters else function(question)

    # **2️⃣ Multi-Keyword Match Check**
    for function_name, keywords in task_groups.items():
        matched_keywords = [kw for kw in keywords if kw in normalized_question]

        if len(matched_keywords) >= 2:
            print(f"✅ Multi-keyword match found ({matched_keywords}), calling {function_name}")
            best_match = globals().get(function_name)
            if best_match:
                sig = inspect.signature(best_match)
                return best_match(question, file_path) if "file_path" in sig.parameters else best_match(question)

    # **3️⃣ Embeddings-Based Fallback (Only if previous checks fail)**
    print("🔍 No exact or multi-keyword match found. Trying embeddings...")

    question_embedding = get_embedding(normalized_question)  # Use normalized question
    if question_embedding is None:
        print("⚠️ Error: Failed to get embedding for question.")
        return {"error": "Embedding service unavailable."}

    best_match = None
    best_score = 0

    for task_name, desc in task_descriptions.items():
        normalized_desc = desc.lower().replace("-", "")  # Normalize descriptions too
        desc_embedding = get_embedding(normalized_desc)

        similarity = sum(a * b for a, b in zip(question_embedding, desc_embedding))  # Dot product similarity

        if similarity > best_score:
            best_score = similarity
            best_match = task_name

    if best_match and best_score > 0.75:
        print(f"✅ Embeddings match found ({best_score}), calling {best_match}")
        best_function = globals().get(best_match)
        if best_function:
            sig = inspect.signature(best_function)
            return best_function(question, file_path) if "file_path" in sig.parameters else best_function(question)

    print("❌ No match found in embeddings.")
    return {"error": "No matching task found."}



# def handle_task(question: str, file: Optional[UploadFile] = None):
    TASK_MAPPING = {
        "https": handle_http_get,
        "google sheets": process_google_sheets_formula,
        "excel": process_excel_formula,
        "multi-cursors": process_text_to_json_multicursors
    }

    task_groups = {
        "extract_csv_from_zip": {"zip", "csv", "answer column"},
        "count_days_in_range": {"date range", "how many"},
        "sort_json_array": {"sort", "json", "array"},
        "process_zip_for_symbol_sum": {"encodings", "UTF-8", "CP-1252"},
        "process_readme_task": {"sha256sum", "npx", " -y prettier"},
        # "calculate_filtered_size": {"zip", "extract", "unzip", "list files", "size", "modified date", "timestamp", "bytes"}
    }

    file_path = None
    if file:
        file_path = handle_file_processing(file)

    print(f"📩 Received question: {question}")
    print(f"🔍 Checking for task match...")

    # **1️⃣ Exact Match Check**
    for keyword, function in TASK_MAPPING.items():
        if keyword in question.lower():
            print(f"✅ Exact match found: {keyword}, calling {function.__name__}")
            sig = inspect.signature(function)
            return function(question, file_path) if "file_path" in sig.parameters else function(question)

    # **2️⃣ Multi-Keyword Match Check**
    for function_name, keywords in task_groups.items():
        normalized_question = question.lower().replace("-", "")
        matched_keywords = [kw for kw in keywords if kw in normalized_question]

        print(f"🔍 Checking multi-keyword match: {function_name} -> Matched keywords: {matched_keywords}")

        if len(matched_keywords) >= 2:  # ✅ If at least one match, call function
            print(f"✅ Multi-keyword match ({matched_keywords}), calling {function_name}")
            best_match = globals()[function_name]
            sig = inspect.signature(best_match)
            return best_match(question, file_path) if "file_path" in sig.parameters else best_match(question)

    # **3️⃣ Embeddings-Based Fallback (Only if previous checks failed)**
    task_descriptions = {  
        "sort_json_array": "Sort a JSON array of objects based on a specific field.",
        "extract_csv_from_zip": "Extract a CSV file from a ZIP archive.",
        "count_days_in_range": "Count how many times a specific weekday appears in a given date range.",
        "process_text_to_json_multicursors": "Download the text file and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}. What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?",
        "calculate_filtered_size": "Download the zip file and extract it. Use ls with options to list all files in the folder along with their date and file size. Whats the total size of all files at least some bytes large and modified on or after the specified date?"
    }

    print("🔍 No exact or multi-keyword match found. Trying embeddings...")

    question_embedding = get_embedding(question)
    if question_embedding is None:
        print("⚠️ Error: Failed to get embedding for question.")
        return {"error": "Embedding service unavailable."}

    best_match = None
    best_score = 0

    for task_name, desc in task_descriptions.items():
        desc_embedding = get_embedding(desc)
        similarity = sum(a * b for a, b in zip(question_embedding, desc_embedding))  # Dot product similarity

        if similarity > best_score:
            best_score = similarity
            best_match = globals()[task_name]

    if best_score > 0.85:  # ✅ Use embeddings only if confidence is high
        print(f"✅ Embeddings match found ({best_score}), calling {best_match.__name__}")
        sig = inspect.signature(best_match)
        return best_match(question, file_path) if "file_path" in sig.parameters else best_match(question)

    return {"error": "No matching task found."}  # ❌ No match found

# def handle_task(question: str, file: Optional[UploadFile] = None):
    TASK_MAPPING = {
        # "sha256sum": process_readme_task,  i changed this because sha256sum was not unique to this question  
        "https": handle_http_get,
        "google sheets": process_google_sheets_formula,
        "excel": process_excel_formula,
        "multi-cursors": process_text_to_json_multicursors
    }

    task_groups = {
        "extract_csv_from_zip": {"zip", "csv", "answer column"},
        "count_days_in_range": {"date range", "how many"},
        "sort_json_array": {"sort", "json", "array"},
        "process_zip_for_symbol_sum": {"encodings", "UTF-8", "CP-1252"},
        "process_readme_task": {"sha256sum", "npx", " -y prettier"},
        "calculate_filtered_size": {}  # Needs at least 2 matches
    }

    # **File Processing**
    file_path = None
    if file:
        file_path = handle_file_processing(file)

    print(f"📩 Received question: {question}")  
    print(f"🔍 Checking for task match...")  

    # **🔹 Combined Matching Process**
    best_match = None
    best_score = 0

    for keyword, function in TASK_MAPPING.items():
        if keyword in question.lower():
            print(f"✅ Exact match found: {keyword}, calling {function.__name__}")
            best_match = function
            break  # ✅ Stop here since we found an exact match

    if not best_match:  # No exact match found, check multi-keyword match
        for function_name, keywords in task_groups.items():
            normalized_question = question.lower().replace("-", "")
            normalized_keywords = {kw.lower().replace("-", "") for kw in keywords}
            matched_keywords = [kw for kw in normalized_keywords if kw in normalized_question]
            print(f"🔍 Checking multi-keyword match: {function_name} -> Matched keywords: {matched_keywords}")

            if len(matched_keywords) >= 2:  # Needs at least 2 keyword matches
                print(f"✅ Multi-keyword match ({matched_keywords}), calling {function_name}")
                best_match = globals()[function_name]
                break  # ✅ Stop once a valid match is found

    if best_match:  
        sig = inspect.signature(best_match)
        result = best_match(question, file_path) if "file_path" in sig.parameters else best_match(question)
        
        print(f"🔍 Raw result from function: {result}")  
        return result  # ✅ Return result immediately

    # **🔹 Embeddings-Based Fallback**
    task_descriptions = {  
        "sort_json_array": "Sort a JSON array of objects based on a specific field.",
        "extract_csv_from_zip": "Extract a CSV file from a ZIP archive.",
        "count_days_in_range": "Count how many times a specific weekday appears in a given date range.",
        "process_text_to_json_multicursors": "Download the text file and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}. What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?",
        "calculate_filtered_size": "Download the zip file and extract it. Use ls with options to list all files in the folder along with their date and file size. What's the total size of all files at least some bytes large and modified on or after the specified date?"
    }

    question_embedding = get_embedding(question)
    for task_name, desc in task_descriptions.items():
        desc_embedding = get_embedding(desc)
        similarity = sum(a * b for a, b in zip(question_embedding, desc_embedding))  # Dot product similarity

        if similarity > best_score:
            best_score = similarity
            best_match = globals()[task_name]

    if best_score > 0.85:  # Only if similarity is high
        print(f"✅ Embeddings match found ({best_score}), calling {best_match.__name__}")
        sig = inspect.signature(best_match)
        result = best_match(question, file_path) if "file_path" in sig.parameters else best_match(question)
        
        print(f"🔍 Raw result from function: {result}")  
        return result  

    return {"error": "No matching task found."}  # ❌ No match found






# def handle_task(question: str, file: Optional[UploadFile] = None):
    TASK_MAPPING = {
        "sha256sum": process_readme_task,  
        "https": handle_http_get,
        "google sheets": process_google_sheets_formula,
        "excel": process_excel_formula,
        "multi-cursors": process_text_to_json_multicursors
    }

    print(f"📩 Received question: {question}")  
    print(f"🔍 Checking for task match...")  

    # **Task Groups with Multi-Keyword Matching**
    task_groups = {
        extract_csv_from_zip: {"zip", "csv", "answer column"},
        count_days_in_range: {"date range", "how many"},
        sort_json_array: {"sort", "json", "array"},
        process_zip_for_symbol_sum: {"encodings", "UTF-8", "CP1252"}  # Needs at least 2 matches
    }

    # **File Processing**
    file_path = None
    if file:
        file_path = handle_file_processing(file)

    # **1️⃣ Exact Single-Keyword Matching (Stops if Found)**
    for keyword, function in TASK_MAPPING.items():
        if keyword in question.lower():
            print(f"✅ Exact match found: {keyword}, calling {function.__name__}")

            sig = inspect.signature(function)
            result = function(question, file_path) if "file_path" in sig.parameters else function(question)
            
            print(f"🔍 Raw result from function: {result}")  
            return result  # ⛔ STOP: Found match, no further checks

    # **2️⃣ Multi-Keyword Matching (At Least 2, Stops if Found)**
    for function, keywords in task_groups.items():
        matched_keywords = [kw for kw in keywords if kw in question.lower()]
        if len(matched_keywords) >= 2:
            print(f"✅ Multi-keyword match ({matched_keywords}), calling {function.__name__}")
            
            sig = inspect.signature(function)
            result = function(question, file_path) if "file_path" in sig.parameters else function(question)
            
            print(f"🔍 Raw result from function: {result}")  
            return result  # ⛔ STOP: Found match, no further checks

    # **3️⃣ Embeddings-Based Fallback (Only Runs If No Exact or Multi-Keyword Match)**
    task_descriptions = {  
        "sort_json_array": "Sort a JSON array of objects based on a specific field.",
        "extract_csv_from_zip": "Extract a CSV file from a ZIP archive.",
        "count_days_in_range": "Count how many times a specific weekday appears in a given date range.",
        "process_text_to_json_multicursors": "Download the text file and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}. What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?",
    }

    question_embedding = get_embedding(question)
    max_score = 0
    best_match = None

    for task_name, desc in task_descriptions.items():
        desc_embedding = get_embedding(desc)
        similarity = sum(a * b for a, b in zip(question_embedding, desc_embedding))  # Dot product similarity

        if similarity > max_score:
            max_score = similarity
            best_match = task_name

    if max_score > 0.85:  # Only if similarity is high
        print(f"✅ Embeddings match found ({max_score}), calling {best_match}")
        function = globals()[best_match]

        sig = inspect.signature(function)
        result = function(question, file_path) if "file_path" in sig.parameters else function(question)
        
        print(f"🔍 Raw result from function: {result}")  
        return result  

    return {"error": "No matching task found."}  # ❌ No match found







































# def handle_task(question: str, file: Optional[UploadFile] = None):
#     TASK_MAPPING = {
#         "sha256sum": process_readme_task,  
#         "https": handle_http_get,
#         "google sheets": process_google_sheets_formula,
#         "excel": process_excel_formula,
#         # Add more tasks here
#     }

#     print(f"📩 Received question: {question}")  
#     print(f"🔍 Checking for task match...")  

#     # Task Groups (Adding `extract_csv_from_zip` dynamically)
#     task_groups = {
#         extract_csv_from_zip: {"zip", "csv", "answer column"},
#         count_days_in_range: {"date range", "how many"},
#     }

#     # Dynamically update TASK_MAPPING
#     for function, keywords in task_groups.items():
#         TASK_MAPPING.update({keyword: function for keyword in keywords})

#     # Check if a file is needed for any matching task
#     file_path = None
#     if file:
#         file_path = handle_file_processing(file)  # ✅ Save file before calling any task

#     # Find the first matching function
#     for keyword, function in TASK_MAPPING.items():
#         print(f"🔎 Checking keyword: {keyword} in question...")
#         if keyword in question.lower():
#             print(f"✅ Match found: {keyword}, calling {function.__name__}")

#             # **Dynamically Check if Function Needs `file_path`**
#             sig = inspect.signature(function)
#             if "file_path" in sig.parameters:
#                 result = function(question, file_path)  # ✅ Pass file if needed
#             else:
#                 result = function(question)  # ✅ Call without file if not needed

#             print(f"🔍 Raw result from function: {result}")  

#             # Ensure result is formatted correctly
#             if isinstance(result, dict):
#                 result = result.get("answer", "Error: Unexpected format")  

#             return result  # ✅ Returns the proper response

#     return {"error": "No matching task found."}  # ❌ No match found





# def handle_task(question: str, file: Optional[UploadFile] = None):
#     TASK_MAPPING = {
#         "sha256sum": process_readme_task,
#         "https": handle_http_get,
#         "google sheets": process_google_sheets_formula,
#         "excel": process_excel_formula,
#     }

#     print(f"📩 Received question: {question}")  # Debugging
#     print(f"🔍 Checking for task match...")  

#     task_groups = {
#         extract_csv_from_zip: {"zip", "csv", "answer column"},
#     }

#     # Only process file if needed
#     file_path = None
#     if file:
#     # and any(keyword in question.lower() for keywords in task_groups.values() for keyword in keywords):
#         file_path = handle_file_processing(file)


#     # Dynamically update TASK_MAPPING
#     for function, keywords in task_groups.items():
#         TASK_MAPPING.update({keyword: function for keyword in keywords})

#     for keyword, function in TASK_MAPPING.items():
#         print(f"🔎 Checking keyword: {keyword} in question...")
#         if keyword in question.lower():
#             print(f"✅ Match found: {keyword}, calling {function.__name__}")
#             result = function(question, file_path)
#             print(f"🔍 Raw result from function: {result}")  # Debugging


#             if function in (task_groups or TASK_MAPPING):
#                 result = function(question, file_path)  # Pass file path to the task
#             else:
#                 result = function(question)  # For functions that don't need file processing
#             # FIX: Ensure result is a string, not a nested dictionary
#             if isinstance(result, dict):  
#                 result = result.get("answer", "Error: Unexpected format")  

#             return result  # ✅ Returns a properly formatted response




























# def handle_task(question: str, file: Optional[UploadFile] = None) -> str:
#     TASK_MAPPING = {
#         "sha256sum": process_readme_task,
#         "https": handle_http_get,
#         # "download": handle_file_processing,
#         "google sheets": process_google_sheets_formula,
#         "excel": process_excel_formula,
#         # "value in answer column of zip file": extract_csv_from_zip,
#     }

#     print(f"📩 Received question: {question}")  # Debugging
#     print(f"🔍 Checking for task match...")  

#     task_groups = {
#     extract_csv_from_zip: {"zip", "csv", "answer column"},
# }
#     file_path = handle_file_processing(file) if file else None
#     # Dynamically update TASK_MAPPING
#     for function, keywords in task_groups.items():
#         TASK_MAPPING.update({keyword: function for keyword in keywords})






#     for keyword, function in TASK_MAPPING.items():
#         print(f"🔎 Checking keyword: {keyword} in question...")
#         if keyword in question.lower():
#             print(f"✅ Match found: {keyword}, calling {function.__name__}")
#             return function(question, file_path)

#     print("❌ No matching task found.")
#     return json.dumps({"answer": "Question type not recognized."})
# def handle_task(question: str, file: Optional[UploadFile] = None) -> str:
#     print(f"📩 Received question: {question}")  # Debugging: Print received question
#     print(f"📂 Received file: {file.filename if file else 'No file provided'}")  # Debugging: Check file

#     TASK_MAPPING = {
#         # ASSIGNMENT 1
#         # Question 2
#         "https": handle_http_get,
#         "download": handle_file_processing,
#         # Question 3
#          "sha256sum": process_readme_task,
#     }
#     print(f"🔍 Matching task for question: {question}")  # Debugging

#     for keyword, function in TASK_MAPPING.items():
#         if keyword in question.lower():
#             return function(question, file)

#     return "Question type not recognized."

# Question 2
def handle_http_get(question: str, file: Optional[UploadFile] = None) -> str:
    # Extract URL using regex
    url_match = re.search(r"https?://\S+", question)
    if not url_match:
        return "Invalid URL in question."
    
    url = url_match.group(0)

    # Extract query parameter using regex (example: "parameter email set to <value>")
    param_match = re.search(r"parameter\s+(\w+)\s+set\s+to\s+([\w@.]+)", question, re.IGNORECASE)
    params = {}

    if param_match:
        param_name, param_value = param_match.groups()
        params[param_name] = param_value

    # Send request with query parameters
    full_url = f"{url}?{urlencode(params)}" if params else url
    response = requests.get(full_url)

    return str(response.json())  # Convert response to string

import os
import tempfile
def handle_file_processing(file: UploadFile) -> str:
    """Saves the uploaded file to the current directory and returns its path."""
    if not file:
        print("📂 No file uploaded.")
        return None

    # Get the current directory
    current_dir = os.getcwd()  # Current working directory
    file_path = os.path.join(current_dir, file.filename)  # Full file path in the current directory

    # Save the file to the current directory
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    print(f"📦 File saved at {file_path}")
    return file_path  # Return the saved file path

# def handle_file_processing(file: UploadFile):
#     """Saves the uploaded file and returns the path in a cross-platform way."""
#     if not file:
#         print("📂 No file uploaded, proceeding without file.")
#         return None

#     temp_dir = tempfile.gettempdir()  # Get the system temp directory
#     temp_path = os.path.join(temp_dir, file.filename)  # Cross-platform path

#     with open(temp_path, "wb") as f:
#         f.write(file.file.read())

#     print(f"📦 File saved at {temp_path}")
#     return temp_path  # Just return the file path, no processing



# def handle_file_processing(question: str, file: Optional[UploadFile] = None) -> str:
#     if file:
#         return f"{question} (File: {file.filename})"  # Attach file name to question
#     return question
# # def handle_file_processing(question: str, file: Optional[UploadFile] = None) -> str:
# #     if file:
# #         return f"Processing file: {file.filename}"
# #     return "No file provided."


# Question 3
import subprocess
import shutil
import os
import traceback
import time
from fastapi import UploadFile

def check_npx():
    """Verify if npx is installed and in PATH."""
    check_cmd = "where npx" if os.name == "nt" else "which npx"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def install_npx():
    """Attempts to install npx if missing."""
    try:
        subprocess.run(["npm", "install", "-g", "npx"], check=True)
        return check_npx()  # Recheck after installation
    except subprocess.CalledProcessError:
        return False

def install_npx_and_prettier():
    """Ensures Node.js, npm, npx, and Prettier are installed."""
    try:
        if not shutil.which("node") or not shutil.which("npm"):
            return "⚠ Node.js or npm is missing. Install it manually."

        if not shutil.which("npx"):
            subprocess.run(["npm", "install", "-g", "npx"], check=True)

        if not shutil.which("prettier"):
            subprocess.run(["npm", "install", "-g", "prettier"], check=True)

        return "✅ npx and Prettier are ready."
    except subprocess.CalledProcessError as e:
        return f"❌ Installation error: {str(e)}"
    

def process_readme_task(question: str, file_path: str) -> dict:
    """Formats the uploaded Markdown file using Prettier and computes its SHA-256 hash."""
    try:
        print("🚀 process_readme_task() is running!")
        # file_path = handle_file_processing(file)  # Save the uploaded file
        if not file_path:
            return {"error": "No file provided or failed to save."}

        print(f"📁 Processing file: {file_path}")
        print(f"🔍 Received question: {question}")  # Now the question is available too!

        # Ensure `npx` is installed
        npx_path = shutil.which("npx")
        if not npx_path:
            return {"error": "❌ npx is not installed or not in PATH."}

        # Run Prettier formatting
        prettier_command = [npx_path, "-y", "prettier@3.4.2", "--write", file_path]
        prettier_result = subprocess.run(prettier_command, capture_output=True, text=True)

        if prettier_result.returncode != 0:
            print(f"❌ Prettier failed: {prettier_result.stderr}")
            return {"error": "Prettier formatting failed."}

        print("✅ Prettier formatting successful")

        # Compute SHA-256 hash
        if os.name == "nt":  # Windows
            print("🟢 Running certutil for hashing on Windows...")
            hash_result = subprocess.run(["certutil", "-hashfile", file_path, "SHA256"],
                                         capture_output=True, text=True, check=True)
            hash_lines = hash_result.stdout.splitlines()
            hash_output = hash_lines[1].strip() if len(hash_lines) > 1 else "❌ Hash extraction failed."
        else:  # Linux/macOS
            print("🟢 Running sha256sum for hashing on Linux/macOS...")
            hash_result = subprocess.run(["sha256sum", file_path], capture_output=True, text=True, check=True)
            hash_output = hash_result.stdout.split()[0]

        print(f"🔢 SHA256 Hash: {hash_output}")
        return hash_output  # Include the question in the response

    except Exception as e:
        print(f"🔥 Unexpected Error: {traceback.format_exc()}")
        return {"error": f"Unexpected error: {str(e)}"}



# def process_readme_task(question: str, file: UploadFile, file_path: str) -> dict:
    """Formats any uploaded Markdown file using Prettier and computes its SHA-256 hash."""
    try:
        print("🚀 process_readme_task() is running!")

        if not file:
            return {"error": "No file provided."}

        # Ensure the file path is valid
        if not file_path:
            return {"error": "File path is missing."}

        file_location = os.path.abspath(file_path)

        print(f"📁 Using file path: {file_location}")

        # Ensure npx is installed
        if not check_npx():
            print("⚠ npx not found! Trying to install...")
            if not install_npx():
                return {"error": "❌ npx is not installed and installation failed."}

        # Install dependencies if needed
        install_result = install_npx_and_prettier()
        if "Error" in install_result:
            return {"error": install_result}

        # Run Prettier dynamically on the uploaded file
        npx_path = shutil.which("npx")  # Get absolute path to npx
        if not npx_path:
            return {"error": "❌ npx is not installed or not in PATH."}

        prettier_command = [npx_path, "-y", "prettier@3.4.2", "--write", file_location]
        prettier_result = subprocess.run(prettier_command, capture_output=True, text=True)

        if prettier_result.returncode != 0:
            print(f"❌ Prettier failed: {prettier_result.stderr}")
            return {"error": "Prettier formatting failed."}

        print("✅ Prettier formatting successful")

        # Compute SHA-256 hash dynamically based on OS
        try:
            if os.name == "nt":  # Windows
                print("🟢 Running certutil for hashing on Windows...")
                hash_result = subprocess.run(["certutil", "-hashfile", file_location, "SHA256"],
                                             capture_output=True, text=True, check=True)
                hash_lines = hash_result.stdout.splitlines()
                hash_output = hash_lines[1].strip() if len(hash_lines) > 1 else "❌ Hash extraction failed."
            else:  # Linux/macOS
                print("🟢 Running sha256sum for hashing on Linux/macOS...")
                hash_result = subprocess.run(["sha256sum", file_location], capture_output=True, text=True, check=True)
                hash_output = hash_result.stdout.split()[0]

            print(f"🔢 SHA256 Hash: {hash_output}")
            return {"answer": hash_output}  # ✅ Ensures correct response format

        except subprocess.CalledProcessError as e:
            print(f"❌ Hashing failed: {e}")
            return {"error": "SHA256 hashing failed."}

    except Exception as e:
        print(f"🔥 Unexpected Error: {traceback.format_exc()}")
        return {"error": f"Unexpected error: {str(e)}"}


# def process_readme_task(question: str, file: UploadFile) -> dict:
#     """Formats any uploaded Markdown file using Prettier and computes its SHA-256 hash."""
#     try:
#         print("🚀 process_readme_task() is running!")

#         if not file:
#             return {"error": "No file provided."}
#         file_location = os.path.abspath(f"./{file.filename}")
#         with open(file_location, "wb") as f:
#             file.file.seek(0)  # Reset file pointer
#             f.write(file.file.read())

#         time.sleep(1)  # Ensure file is properly saved before processing
#         print(f"📁 File saved as: {file_location}")

#         # Ensure npx is installed
#         if not check_npx():
#             print("⚠ npx not found! Trying to install...")
#             if not install_npx():
#                 return {"error": "❌ npx is not installed and installation failed."}

#         # Install dependencies if needed
#         install_result = install_npx_and_prettier()
#         if "Error" in install_result:
#             return {"error": install_result}

#         # Run Prettier dynamically on the uploaded file
#         npx_path = shutil.which("npx")  # Get absolute path to npx
#         if not npx_path:
#             return {"error": "❌ npx is not installed or not in PATH."}

#         prettier_command = [npx_path, "-y", "prettier@3.4.2", "--write", file_location]
#         prettier_result = subprocess.run(prettier_command, capture_output=True, text=True)

#         if prettier_result.returncode != 0:
#             print(f"❌ Prettier failed: {prettier_result.stderr}")
#             return {"error": "Prettier formatting failed."}

#         print("✅ Prettier formatting successful")

#         # Compute SHA-256 hash dynamically based on OS
#         try:
#             if os.name == "nt":  # Windows
#                 print("🟢 Running certutil for hashing on Windows...")
#                 hash_result = subprocess.run(["certutil", "-hashfile", file_location, "SHA256"],
#                                              capture_output=True, text=True, check=True)
#                 hash_lines = hash_result.stdout.splitlines()
#                 hash_output = hash_lines[1].strip() if len(hash_lines) > 1 else "❌ Hash extraction failed."
#             else:  # Linux/macOS
#                 print("🟢 Running sha256sum for hashing on Linux/macOS...")
#                 hash_result = subprocess.run(["sha256sum", file_location], capture_output=True, text=True, check=True)
#                 hash_output = hash_result.stdout.split()[0]

#             print(f"🔢 SHA256 Hash: {hash_output}")
#             return {"answer": hash_output}

#         except subprocess.CalledProcessError as e:
#             print(f"❌ Hashing failed: {e}")
#             return {"error": "SHA256 hashing failed."}

#     except Exception as e:
#         print(f"🔥 Unexpected Error: {traceback.format_exc()}")
#         return {"error": f"Unexpected error: {str(e)}"}


# Question 4
import re

def process_google_sheets_formula(question, file=None):
    """
    Parses a question string and computes the equivalent of:
    =SUM(ARRAY_CONSTRAIN(SEQUENCE(cols, cols, start, step), 1, count))
    """

    try:
        # Extract numerical values using regex
        match = re.search(r'cols\s*=\s*(\d+),\s*start\s*=\s*(\d+),\s*step\s*=\s*(\d+),\s*count\s*=\s*(\d+)', question)
        if not match:
            return {"answer": "Error: Could not extract parameters from the question."}

        # Convert extracted values to integers
        cols, start, step, count = map(int, match.groups())

        # Validate input constraints
        if cols <= 0 or count <= 0:
            return {"answer": "Error: 'cols' and 'count' must be positive integers."}

        # Generate the first row dynamically
        first_row = [start + i * step for i in range(cols)]

        # Compute the sum of the first `count` elements
        result = sum(first_row[:min(count, cols)])

        return {"answer": str(result)}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}


# Question 5
import numpy as np

def process_excel_formula(question, file=None):
    """
    Process a dynamically generated Excel formula equivalent in Python.

    The expected format of the question:
    In Excel, the formula `=SUM(TAKE(SORTBY({values}, {sort_keys}), 1, take_count))` computes a sum.
    Compute the equivalent result for: values = [...], sort_keys = [...], take_count = N.
    """
    try:
        # Extract values using regex
        match = re.search(
            r"values\s*=\s*\[([\d,\s]+)\],\s*sort_keys\s*=\s*\[([\d,\s]+)\],\s*take_count\s*=\s*(\d+)",
            question
        )
        if not match:
            return {"answer": "Invalid input format."}

        # Parse extracted values
        values = list(map(int, match.group(1).split(",")))
        sort_keys = list(map(int, match.group(2).split(",")))
        take_count = int(match.group(3))

        # Ensure values and sort_keys have the same length
        if len(values) != len(sort_keys):
            return {"answer": "Error: 'values' and 'sort_keys' must have the same length."}

        # Sort values based on sort_keys
        sorted_values = [v for _, v in sorted(zip(sort_keys, values))]

        # Take the first 'take_count' values and sum them
        result = sum(sorted_values[:take_count])

        return {"answer": str(result)}

    except Exception as e:
        return {"answer": str(e)}


# Question 7
import re
from datetime import datetime, timedelta

def count_days_in_range(question: str) -> dict:
    """Extracts the date range and weekday from a question and counts occurrences of that weekday."""

    # Extract the start date and end date using regex
    match = re.search(r"(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})", question)
    if not match:
        return {"error": "Invalid date range format."}

    start_date, end_date = match.groups()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start > end:
            return {"error": "Start date must be before the end date."}

        # Detect the weekday dynamically
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        words = question.split()  # Tokenize the question into words
        target_day = next((word for word in words if word in weekdays), "Wednesday")  # Default to Wednesday

        if target_day not in weekdays:
            return {"error": f"Invalid day name detected: {target_day}"}

        target_weekday = weekdays.index(target_day)

        # Count occurrences of the target weekday
        count = sum(1 for d in range((end - start).days + 1) if (start + timedelta(days=d)).weekday() == target_weekday)

        return {"answer": count}

    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}



# Question 8
import os
import zipfile
import pandas as pd
import tempfile

def extract_csv_from_zip(question, file_path):
    """
    Extract a CSV file from a ZIP archive and return the first value from the 'answer' column.
    """

    print(f"📩 Processing ZIP file: {file_path}")  # Debugging log

    if not file_path.endswith('.zip'):
        print("❌ Error: File is not a ZIP archive")
        return {"answer": "Error: Uploaded file is not a ZIP archive."}

    with tempfile.TemporaryDirectory() as temp_dir:  # Temporary directory for extracted files
        try:
            # Extract files from ZIP
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if not csv_files:
                    print("❌ Error: No CSV file found in ZIP")
                    return {"answer": "Error: No CSV file found in the ZIP archive."}

                # Extract first CSV file
                first_csv = csv_files[0]
                extracted_path = zip_ref.extract(first_csv, temp_dir)

            print(f"📖 Reading CSV file: {extracted_path}")

            # Read CSV file
            df = pd.read_csv(extracted_path)
            print(f"📊 CSV columns: {df.columns.tolist()}")

            if "answer" not in df.columns:
                print("❌ Error: 'answer' column missing")
                return {"answer": "Error: Column 'answer' not found in the CSV file."}

            # Get the first value in the 'answer' column
            answer_value = df["answer"].iloc[0]
            print(f"✅ Extracted Answer: {answer_value}")

            # 🔥 FIX: Return a properly formatted JSON object
            return str(answer_value)

        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"answer": f"Error: {str(e)}"}

# import os
# import zipfile
# import pandas as pd
# import tempfile
# import shutil

# def extract_csv_from_zip(question, file_path):
#     """
#     Extract a CSV file from a ZIP archive and return the first value from the 'answer' column.
#     """

#     print(f"📩 Processing ZIP file: {file_path}")  # Debugging log

#     if not file_path.endswith('.zip'):
#         print("❌ Error: File is not a ZIP archive")
#         return {"answer": "Error: Uploaded file is not a ZIP archive."}

#     with tempfile.TemporaryDirectory() as temp_dir:  # Temporary directory for extracted files
#         try:
#             # Extract files from ZIP
#             with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                 csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
#                 if not csv_files:
#                     print("❌ Error: No CSV file found in ZIP")
#                     return {"answer": "Error: No CSV file found in the ZIP archive."}

#                 # Extract first CSV file
#                 first_csv = csv_files[0]
#                 extracted_path = zip_ref.extract(first_csv, temp_dir)

#             print(f"📖 Reading CSV file: {extracted_path}")

#             # Read CSV file
#             df = pd.read_csv(extracted_path)
#             print(f"📊 CSV columns: {df.columns.tolist()}")

#             if "answer" not in df.columns:
#                 print("❌ Error: 'answer' column missing")
#                 return {"answer": "Error: Column 'answer' not found in the CSV file."}

#             # Get the first value in the 'answer' column
#             answer_value = df["answer"].iloc[0]
#             print(f"✅ Extracted Answer: {answer_value}")

#             return {"answer": str(answer_value)}

#         except Exception as e:
#             print(f"❌ Exception: {str(e)}")
#             return {"answer": f"Error: {str(e)}"}





# Question 9
import json
import re

def sort_json_array(question):
    # Extract JSON array using regex
    match = re.search(r'\[.*\]', question, re.DOTALL)
    if not match:
        raise ValueError("No JSON array found in question")

    json_str = match.group(0)
    data = json.loads(json_str)

    # Extract sorting keys dynamically from the question
    sorting_keys = re.findall(r'by the value of the (\w+) field', question)

    # Sort the list based on extracted keys
    sorted_data = sorted(data, key=lambda x: tuple(x[key] for key in sorting_keys))

    return sorted_data  # ✅ Return as a proper JSON object, NOT a string


# Question 10
import json
import hashlib
import os
def process_text_to_json_multicursors(question, file_path):
    filename = os.path.basename(file_path)

    # Read file contents
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return {"error": f"File {filename} not found."}

    # Convert key=value lines into a dictionary
    json_obj = {}
    for line in lines:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            json_obj[key.strip()] = value.strip()

    json_str = json.dumps(json_obj, separators=(",", ":"))

    # 🔹 Generate SHA-256 hash locally
    json_hash = hashlib.sha256(json_str.encode()).hexdigest()

    return {"answer": json_hash}





# import json
# import requests
# import os

# def process_text_to_json_multicursors(question, file_path):
#     filename = os.path.basename(file_path)

#     # Read file contents
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             lines = file.readlines()
#     except FileNotFoundError:
#         return {"error": f"File {filename} not found."}

#     # Convert key=value lines into a dictionary
#     json_obj = {}
#     for line in lines:
#         if "=" in line:
#             key, value = line.strip().split("=", 1)
#             json_obj[key.strip()] = value.strip()

#     json_str = json.dumps(json_obj, separators=(",", ":"))

#     # Send request to hash API
#     try:
#         url = f"https://tools-in-data-science.pages.dev/jsonhash?json={json_str}"
#         response = requests.get(url)
#         response.raise_for_status()  # Ensure the request didn't fail

#         # ✅ Debugging: Print response before parsing
#         print("Raw API Response:", response.text)

#         # Parse JSON only if response is not empty
#         if response.text.strip():
#             hash_result = response.json().get("hash", "Error: Hash key not found")
#         else:
#             hash_result = "Error: Empty response from server"

#     except requests.RequestException as e:
#         return {"error": f"Failed to get hash: {str(e)}"}
#     except json.JSONDecodeError:
#         return {"error": "Failed to parse JSON from response"}

#     return {"filename": filename, "json": json_str, "hash": hash_result}


# Question 12
import os
import zipfile
import tempfile
import pandas as pd
import chardet

def process_zip_for_symbol_sum(question, file_path):
    """
    Extracts files from a ZIP archive and calculates the sum of values for symbols (‘, ˆ, š).
    """

    print(f"📩 Processing ZIP file: {file_path}")  # Debug log

    if not file_path.endswith('.zip'):
        print("❌ Error: File is not a ZIP archive")
        return {"answer": "Error: Uploaded file is not a ZIP archive."}

    with tempfile.TemporaryDirectory() as temp_dir:  # Temporary directory for extraction
        try:
            # Extract files
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            print(f"📂 Files extracted to: {temp_dir}")

            target_symbols = {'‘', 'ˆ', 'š'}
            total_sum = 0

            # Process each extracted file
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)

                # Detect encoding
                with open(file_path, 'rb') as f:
                    result = chardet.detect(f.read(100000))  # Read a chunk to detect encoding
                encoding = result['encoding']

                # Determine delimiter based on file extension
                delimiter = ',' if filename.endswith('.csv') else '\t'

                try:
                    # Read file
                    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

                    # Normalize column names
                    df.columns = df.columns.str.strip().str.lower()

                    # Ensure required columns exist
                    if "symbol" in df.columns and "value" in df.columns:
                        # Sum values for matching symbols
                        total_sum += df[df["symbol"].isin(target_symbols)]["value"].sum()

                except Exception as e:
                    print(f"❌ Error processing {filename}: {str(e)}")
                    return {"answer": f"Error processing {filename}: {str(e)}"}

            print(f"✅ Total Sum: {total_sum}")
            return {"answer": str(total_sum)}

        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"answer": f"Error: {str(e)}"}


# Question 15
import os
import zipfile
from datetime import datetime
import os
import zipfile
import re
from datetime import datetime

def extract_number(text):
    """Extracts the first numeric value from a given text."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def extract_datetime(text):
    """Extracts a date-time string and converts it into a datetime object."""
    date_match = re.search(r'(\w{3}, \d{1,2} \w{3}, \d{4}, \d{1,2}:\d{2} (?:am|pm) IST)', text, re.IGNORECASE)
    if date_match:
        try:
            return datetime.strptime(date_match.group(), "%a, %d %b, %Y, %I:%M %p IST")
        except ValueError:
            return None
    return None

def calculate_filtered_size(question, file_path):
    """
    Extracts the ZIP file, lists all files with their sizes and modification dates, 
    and calculates the total size of files meeting the specified criteria:
    - File size >= (extracted from the question)
    - Last modified on or after (extracted from the question)

    Parameters:
    - question (str): The task description containing the dynamic parameters.
    - file_path (str): Path to the ZIP file.

    Returns:
    - str: Total size of the filtered files in bytes.
    """
    
    # **Extract parameters dynamically from the question**
    min_size = extract_number(question)  # Extract file size
    min_date = extract_datetime(question)  # Extract date-time
    
    if min_size is None or min_date is None:
        return {"error": "Could not extract required parameters from the question."}
    
    # **Extract ZIP contents**
    extract_dir = "extracted_files"
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # **Calculate total size**
    total_size = 0

    for root, _, files in os.walk(extract_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_mod_date = datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_size >= min_size and file_mod_date >= min_date:
                total_size += file_size

    return str(total_size)


# def calculate_filtered_size(question, file_path):
#     """
#     Extracts the ZIP file, lists all files with their sizes and modification dates, 
#     and calculates the total size of files meeting the specified criteria:
#     - File size >= 4346 bytes
#     - Last modified on or after "Wed, 26 Jan, 2005, 6:23 am IST"
    
#     Parameters:
#     - question (str): The task description (not used in logic, included for consistency).
#     - file_path (str): Path to the ZIP file.

#     Returns:
#     - str: Total size of the filtered files in bytes.
#     """

#     # Define the minimum file size in bytes
#     min_size = 4346  

#     # Define the minimum modification date as per the question
#     min_date_str = "Wed, 26 Jan, 2005, 6:23 am IST"
#     date_format = "%a, %d %b, %Y, %I:%M %p IST"

#     try:
#         # Convert the string to a datetime object
#         min_date = datetime.strptime(min_date_str, date_format)
#     except ValueError:
#         raise ValueError(f"Invalid date format: {min_date_str}. Expected format: '{date_format}'")

#     # Create a temporary directory to extract files
#     extract_dir = "extracted_files"
#     os.makedirs(extract_dir, exist_ok=True)

#     # Extract the ZIP file
#     with zipfile.ZipFile(file_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_dir)

#     # Initialize total size
#     total_size = 0

#     # List all extracted files
#     for root, _, files in os.walk(extract_dir):
#         for file in files:
#             file_path = os.path.join(root, file)

#             # Get file size
#             file_size = os.path.getsize(file_path)

#             # Get file modification time
#             mod_time = os.path.getmtime(file_path)
#             file_mod_date = datetime.fromtimestamp(mod_time)

#             # Check if the file meets the criteria
#             if file_size >= min_size and file_mod_date >= min_date:
#                 total_size += file_size

#     # Cleanup extracted files (optional)
#     # shutil.rmtree(extract_dir)

#     return str(total_size)




# def calculate_filtered_size(zip_path, min_size, min_date):
    extract_folder = zip_path.replace(".zip", "")

    # Ensure extraction preserves timestamps
    if os.name == "nt":  # Windows: Use 7-Zip
        subprocess.run(["7z", "x", zip_path, f"-o{extract_folder}", "-y"], check=True)
    else:  # Linux/macOS: Use unzip
        subprocess.run(["unzip", "-o", zip_path, "-d", extract_folder], check=True)

    total_size = 0
    min_date_obj = datetime.strptime(min_date, "%a, %d %b, %Y, %I:%M %p %Z")

    # List extracted files and filter by conditions
    for file in os.listdir(extract_folder):
        file_path = os.path.join(extract_folder, file)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            # Apply filters
            if file_size >= min_size and mod_time >= min_date_obj:
                total_size += file_size

    return {"total_size": total_size}


# Question 17
import os
import zipfile
def count_different_lines(question, file_path):
    """
    Extracts the ZIP file and compares two nearly identical `.txt` files to count 
    how many lines are different.

    Parameters:
    - question (str): The task description (used to extract dynamic parameters).
    - file_path (str): Path to the ZIP file.

    Returns:
    - str: Number of differing lines between the two text files.
    """

    # Create a temporary directory to extract files
    extract_dir = "extracted_files"
    os.makedirs(extract_dir, exist_ok=True)

    # Extract ZIP file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Find all text files in extracted directory
    text_files = [f for f in os.listdir(extract_dir) if f.endswith(".txt")]

    if len(text_files) < 2:
        return {"error": "Less than two text files found in the ZIP archive."}

    # Sort file names to ensure consistency
    text_files.sort()

    file1_path = os.path.join(extract_dir, text_files[0])
    file2_path = os.path.join(extract_dir, text_files[1])

    # Compare line-by-line
    diff_count = 0
    with open(file1_path, "r", encoding="utf-8") as f1, open(file2_path, "r", encoding="utf-8") as f2:
        for line1, line2 in zip(f1, f2):
            if line1.strip() != line2.strip():
                diff_count += 1

    return str(diff_count)  # Return the number of different lines as a string





# ASSIGNMENT 2


# Question 5
import re
import json
import numpy as np
from PIL import Image
import colorsys
from bs4 import BeautifulSoup  # To handle HTML input
def process_light_pixel_task(question, file_path):
    """
    Extracts Python code, fixes errors, and processes an image to count bright pixels.

    Parameters:
    - question (str): The task description (used for extracting brightness threshold).
    - file_path (str): Path to the image file.

    Returns:
    - str: The number of pixels exceeding the brightness threshold.
    """
    
    def extract_python_code(question):
        """Extracts Python code from JSON or HTML question formats."""
        try:
            data = json.loads(question)
            if "code" in data:
                return data["code"]
        except json.JSONDecodeError:
            pass  # Not JSON, proceed to HTML extraction

        soup = BeautifulSoup(question, "html.parser")
        code_blocks = soup.find_all("code")
        return "\n".join([block.get_text() for block in code_blocks]) if code_blocks else ""

    # Extract brightness threshold dynamically
    match = re.search(r"lightness\s*>\s*([\d\.]+)", question)
    threshold = float(match.group(1)) if match else 0.312  # Default to 0.312

    # Open the image and process brightness
    image = Image.open(file_path)
    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = np.sum(lightness > threshold)

    return str(light_pixels)





# Assignment 4


# Question 3- Still confused about this, recheck whether we need markdown, api endpoint or what
# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from bs4 import BeautifulSoup
# import httpx
# import re

# from fastapi import FastAPI
# app = FastAPI()

# # Enable CORS for all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"

# @app.get("/api/outline")
# async def get_country_outline(country: str = Query(..., min_length=1, description="Country name to fetch outline for")):
#     """
#     Fetch the Wikipedia page for the given country, extract headings, and return a Markdown outline.
#     """
#     url = f"{WIKIPEDIA_BASE_URL}{country.replace(' ', '_')}"

#     try:
#         # Fetch Wikipedia page content
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             response.raise_for_status()

#     except httpx.HTTPStatusError:
#         raise HTTPException(status_code=404, detail=f"Could not find Wikipedia page for '{country}'.")

#     # Parse HTML and extract headings
#     soup = BeautifulSoup(response.text, "html.parser")
#     headings = soup.find_all(re.compile(r"^h[1-6]$"))

#     if not headings:
#         raise HTTPException(status_code=404, detail=f"No headings found on the Wikipedia page for '{country}'.")

#     # Generate Markdown outline
#     markdown_outline = ["## Contents", f"# {country}\n"]

#     for heading in headings:
#         level = int(heading.name[1])  # Extract the level from the tag (h1 -> 1, h2 -> 2, etc.)
#         text = heading.get_text(strip=True)
#         markdown_outline.append(f"{'#' * level} {text}")

#     return {"outline": "\n".join(markdown_outline)}








# Instructions to run
# 1. Save this file (e.g., `main.py`).
# 2. Open a terminal and install dependencies:
#    pip install fastapi httpx beautifulsoup4 uvicorn
# 3. Run the app:
#    uvicorn main:app --reload
# 4. Test the API at: http://localhost:8000/api/outline?country=CountryName



# from fastapi import FastAPI, Query
# from fastapi.responses import JSONResponse
# import requests
# from bs4 import BeautifulSoup
# import re

# app = FastAPI()

# # Enable CORS (allows access from any origin)
# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_methods=["GET"],  # Allow GET requests
#     allow_headers=["*"],
# )

# @app.get("/api/outline")
# def get_wikipedia_outline(country: str = Query(..., title="Country Name")):
#     """
#     Fetches the Wikipedia page for the given country and extracts its headings (H1-H6),
#     returning them as a Markdown outline in JSON format.
#     """

#     # Format country name for Wikipedia URL
#     country_formatted = country.strip().replace(" ", "_")
#     url = f"https://en.wikipedia.org/wiki/{country_formatted}"

#     # Fetch Wikipedia page
#     response = requests.get(url)
#     if response.status_code != 200:
#         return JSONResponse(content={"error": f"Wikipedia page for '{country}' not found."}, status_code=404)

#     # Parse HTML and extract headings (H1-H6)
#     soup = BeautifulSoup(response.text, "html.parser")
#     headings = soup.find_all(re.compile("^h[1-6]$"))

#     # Generate Markdown Outline
#     markdown_outline = "## Contents\n\n"
#     markdown_outline += f"# {country}\n\n"  # Add country name as H1

#     for tag in headings:
#         level = int(tag.name[1])  # Extract heading level (h1-h6)
#         markdown_outline += f"{'#' * level} {tag.get_text(strip=True)}\n\n"

#     return JSONResponse(content={"outline": markdown_outline.strip()})

import requests
from bs4 import BeautifulSoup
import re

def fetch_wikipedia_outline(question):
    """
    Extracts country name dynamically from the question, fetches Wikipedia page,
    extracts headings (H1-H6), and returns a Markdown outline.
    """

    # Extract country name using regex (assumes "for [Country]" pattern)
    match = re.search(r"for (\w[\w\s]+)", question, re.IGNORECASE)
    if not match:
        return "Error: No valid country parameter found."

    country = match.group(1).strip().replace(" ", "_")  # Format for Wikipedia URL

    # Fetch Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: Wikipedia page for '{country}' not found."

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(re.compile("^h[1-6]$"))

    # Generate Markdown Outline
    markdown_outline = "## Contents\n\n"
    for tag in headings:
        level = int(tag.name[1])  # Extract heading level (h1-h6)
        markdown_outline += f"{'#' * level} {tag.get_text(strip=True)}\n\n"

    return markdown_outline.strip()





# Question 4
import requests
import re
import pandas as pd
def get_weather_forecast(question: str):
    """
    Fetches the weather forecast description for a given city using BBC Weather Broker API.
    Returns a JSON object mapping dates to weather descriptions.
    """

    # Extract city name from the question
    # Extract city name correctly
    city = question.replace("What is the JSON weather forecast description for", "").strip().strip("?").strip()
    
    print(f"🌍 Received question: {question}")
    print(f"🏙️ Extracted City: {city}")

    # Step 1: Get Location ID from BBC Locator API
    locator_url = f"https://locator-service.api.bbci.co.uk/locations?api_key=AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv&s={city}&stack=aws&locale=en&filter=international&place-types=settlement%2Cairport%2Cdistrict&order=importance&a=true&format=json"
    
    locator_response = requests.get(locator_url)
    locator_data = locator_response.json()

    results = locator_data.get("response", {}).get("results", {}).get("results", [])
    if not results:
        return {"answer": {"error": f"Location ID not found for {city}"}}

    location_id = results[0]["id"]
    print(f"📍 Found Location ID: {location_id}")

        # Step 2: Fetch BBC Weather Page
    weather_url = f"https://www.bbc.com/weather/{location_id}"
    response = requests.get(weather_url)

    if response.status_code != 200:
        print(f"🚨 Failed to fetch weather page! Status Code: {response.status_code}")
        return {"answer": f"Failed to fetch weather page for {city}"}

    # Step 3: Parse the Weather Page with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Step 4: Extract Weather Descriptions (Based on Actual Inspection)
    descriptions = soup.find_all("div", class_="wr-day-summary")  # Correct class name

    if not descriptions:
        return {"answer": f"No forecast data available for {city}"}

    # ✅ Step 1: Split descriptions properly using regex
    weather_descriptions = []
    for desc in descriptions:
        text = desc.get_text(strip=True)  # Extract text safely
        split_descriptions = re.findall(r'[a-zA-Z][^A-Z]*', text)  # Properly split descriptions
        weather_descriptions.extend([s.strip() for s in split_descriptions if s.strip()])  # Clean and store

# ✅ Step 2: Generate Date List (starting from today)
    datelist = pd.date_range(datetime.today(), periods=len(weather_descriptions)).tolist()
    datelist = [date.strftime('%Y-%m-%d') for date in datelist]  # Correct format

# ✅ Step 3: Create JSON Dictionary
    forecast_data = {datelist[i]: weather_descriptions[i] for i in range(len(datelist))}

# ✅ Output JSON
    return forecast_data


# Question 5
import re
import requests
def extract_query_params(question: str):
    """
    Extracts city, country, and bounding box parameter (min/max lat/lon) from the input question.
    
    Parameters:
        question (str): The natural language question asked by the user.

    Returns:
        dict: Extracted city, country, and bounding box parameter.
    """
    # Define mappings for possible bounding box terms
    bbox_mapping = {
        "minimum latitude": "min_lat",
        "maximum latitude": "max_lat",
        "minimum longitude": "min_lon",
        "maximum longitude": "max_lon"
    }

    # Regex pattern to find city and country
    city_country_pattern = re.search(r"city (\w+) in the country (\w+)", question, re.IGNORECASE)

    if not city_country_pattern:
        return {"error": "Could not extract city and country from the question."}

    city = city_country_pattern.group(1)
    country = city_country_pattern.group(2)

    # Find which bounding box value is needed
    bbox_type = None
    for key in bbox_mapping:
        if key in question.lower():
            bbox_type = bbox_mapping[key]
            break

    if not bbox_type:
        return {"error": "Could not determine bounding box parameter."}

    return {"city": city, "country": country, "bbox_type": bbox_type}
def using_nominatim_api(question: str):
    """
    Extracts parameters from the question and fetches the requested geospatial data.

    Parameters:
        question (str): The natural language question asked by the user.

    Returns:
        dict: JSON response containing the requested geospatial data.
    """
    params = extract_query_params(question)
    
    if "error" in params:
        return params

    city, country, bbox_type = params["city"], params["country"], params["bbox_type"]

    base_url = "https://nominatim.openstreetmap.org/search"
    api_params = {
        "city": city,
        "country": country,
        "format": "json",
        "limit": 1
    }

    response = requests.get(base_url, params=api_params, headers={"User-Agent": "myGeocoder"})
    
    if response.status_code != 200:
        return {"error": "Failed to retrieve data from Nominatim API"}

    data = response.json()
    if not data:
        return {"error": f"No results found for {city}, {country}"}

    bounding_box = data[0].get("boundingbox", [])
    
    if len(bounding_box) != 4:
        return {"error": "Bounding box data not available"}

    # Map bounding box response
    bbox_values = {
        "min_lat": bounding_box[0],
        "max_lat": bounding_box[1],
        "min_lon": bounding_box[2],
        "max_lon": bounding_box[3]
    }

    return bbox_values.get(bbox_type, "Unknown")


# Question 6
import requests
import re
from bs4 import BeautifulSoup
HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search?query="
HN_ITEM_URL = "https://news.ycombinator.com/item?id="
def extract_min_max_points(question):
    """Extract min/max point constraints from the question."""
    min_points, max_points = None, None

    min_match = re.search(r"at least (\d+) points", question)
    max_match = re.search(r"at most (\d+) points", question)

    if min_match:
        min_points = int(min_match.group(1))
    if max_match:
        max_points = int(max_match.group(1))

    return min_points, max_points
def get_hacker_news_posts(query):
    """Fetch the latest Hacker News posts mentioning the query."""
    response = requests.get(f"{HN_SEARCH_URL}{query}&tags=story&hitsPerPage=10")
    if response.status_code != 200:
        return []

    data = response.json()
    return [
        {"title": item["title"], "url": HN_ITEM_URL + str(item["objectID"])}
        for item in data.get("hits", [])
    ]
def get_post_points(post_url):
    """Scrape points of a Hacker News post."""
    response = requests.get(post_url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    points_tag = soup.find("span", class_="score")

    if points_tag:
        return int(points_tag.text.split()[0])  # Extract numeric points
    return None
def search_hn_latest(question):
    """Find the latest HN post matching the given constraints."""
    min_points, max_points = extract_min_max_points(question)
    query_topic = re.search(r"mentioning (.+?) having", question)
    
    if not query_topic:
        return {"answer": "Invalid question format"}

    query = query_topic.group(1)
    posts = get_hacker_news_posts(query)

    for post in posts:
        post["points"] = get_post_points(post["url"])

    filtered_posts = [
        post for post in posts
        if post["points"] is not None
        and (min_points is None or post["points"] >= min_points)
        and (max_points is None or post["points"] <= max_points)
    ]

    if filtered_posts:
        latest_post = max(filtered_posts, key=lambda x: x["points"])  # Highest points
        return latest_post["url"]

    return {"answer": "No matching post found"}


# Question 9
import re
import pandas as pd
import camelot
def calculate_total_marks(question, file_path):
    """Extracts parameters from the question and calculates total marks from a PDF file."""
    
    print(f"📌 Received Question: {repr(question)}")  # Debugging print
    print(f"🔎 Words in Question: {question.split()}")  # Word-by-word check

    # 🔍 Updated regex (more flexible)
    pattern = r"total\s+(\w+)\s+marks.*?(\d+)\s+(?:or\s+)?(more|less|at\s+least|at\s+most)?\s*marks\s+in\s+(\w+).*?groups\s+(\d+)-(\d+)"

    match = re.search(pattern, question, re.IGNORECASE)

    if not match:
        print("❌ Regex match failed! (Possible extra spaces or incorrect format)")
        return {"error": "Invalid question format"}

    # Extract parameters
    subject = match.group(1).capitalize()    # e.g., "Maths"
    min_marks = int(match.group(2))          # e.g., 10
    comparison = match.group(3) if match.group(3) else "more"  # Default to "more"
    filter_subject = match.group(4).capitalize()  # e.g., "Biology"
    group_start = int(match.group(5))        # e.g., 59
    group_end = int(match.group(6))          # e.g., 83

    print(f"✅ Extracted Parameters: {subject}, {min_marks} ({comparison}), {filter_subject}, Groups {group_start}-{group_end}")

        # ✅ Convert groups to PDF page numbers dynamically
    page_start = group_start  # Assuming 1 group = 1 page
    page_end = group_end
    pages = f"{page_start}-{page_end}"

    print(f"✅ Extracted Parameters: {subject}, {min_marks} ({comparison}), {filter_subject}, Pages {pages}")

    try:
        # ✅ Extract tables from the relevant pages
        tables = camelot.read_pdf(file_path, pages=pages, flavor='stream')

        if tables.n == 0:
            return {"error": "No tables found in the PDF"}

        # ✅ Combine all extracted tables
        df_list = [table.df for table in tables]
        combined_df = pd.concat(df_list, ignore_index=True)

        # ✅ Identify the row containing column headers dynamically
        header_row_idx = combined_df[combined_df.iloc[:, 0] == "Maths"].index[0]
        data = combined_df.iloc[header_row_idx + 1:].reset_index(drop=True)

        # ✅ Rename columns based on extracted header row
        data.columns = ["Maths", "Physics", "English", "Economics", "Biology"]  # Adjust as needed

        # ✅ Convert relevant columns to numeric
        data[subject] = pd.to_numeric(data[subject], errors="coerce")
        data[filter_subject] = pd.to_numeric(data[filter_subject], errors="coerce")
        data.dropna(subset=[subject, filter_subject], inplace=True)

        # ✅ Apply filtering based on the extracted parameters
        if comparison in ["more", "at least", ]:
            filtered_data = data[data[filter_subject] >= min_marks]
        else:  # "less" or "at most"
            filtered_data = data[data[filter_subject] <= min_marks]

        # ✅ Calculate total Maths marks
        total_marks = filtered_data[subject].sum()

        return str(int(total_marks))

    except Exception as e:
        return {"error": str(e)}





# ASSIGNMENT 5

# Question 2
import re
def count_unique_students(question, file_path):  # Accept both arguments (ignore 'question')
    try:
        # Read the file
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Regular expression to extract student IDs
        pattern = r"[-]\s*([\w\d]+)\s*::?Marks"
        student_ids = set()  # Using a set to ensure unique student IDs

        for line in lines:
            match = re.search(pattern, line.strip())
            if match:
                student_id = match.group(1).strip()  # Extract student ID
                student_ids.add(student_id)  # Add to set (automatically removes duplicates)

        # Return the number of unique student IDs
        return {"answer": len(student_ids)}

    except Exception as e:
        return {"error": str(e)}


# Question 3
import gzip
import re
from datetime import datetime, timezone, timedelta
# Define regex pattern for parsing log entries
log_pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\S+) ".*?" ".*?"'
)
# Convert GMT-0500 to proper timezone offset
GMT_OFFSET = timedelta(hours=-5)
# Map weekday names to numbers
DAYS_MAPPING = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6
}
def extract_parameters(question):
    """
    Extracts dynamic parameters from the question using regex.
    Supports both 'telugu' and '/telugu/' formats.
    """
    match = re.search(r'pages under\s*[/"]?(.*?)["/]?\s*from\s*(\d+):\d+\s*until before\s*(\d+):\d+\s*on\s*(\w+)', question)
    if not match:
        return None

    target_path, start_hour, end_hour, target_day = match.groups()
    target_path = target_path.strip("/")  # Remove leading/trailing slashes
    start_hour, end_hour = int(start_hour), int(end_hour)

    # Normalize the day name (handle "Mondays" → "Monday")
    target_day = target_day.lower().rstrip('s')
    target_day_num = DAYS_MAPPING.get(target_day)

    if target_day_num is None:
        return None  # Invalid day

    return target_path, start_hour, end_hour, target_day_num
def is_valid_time(log_time, target_day, start_hour, end_hour):
    """
    Check if the log entry falls on the correct weekday and time range.
    """
    try:
        # Convert log timestamp to datetime object
        log_dt = datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S %z")
        log_dt = log_dt.astimezone(timezone(GMT_OFFSET))  # Apply GMT-0500 offset

        # Ensure correct day and time range
        return log_dt.weekday() == target_day and start_hour <= log_dt.hour < end_hour
    except ValueError:
        return False
def count_successful_requests(question, file_path):
    """
    Count successful GET requests for a specified path on a given weekday within a time range.
    """
    # Extract parameters dynamically from the question
    params = extract_parameters(question)
    if not params:
        return "Error: Could not extract parameters from the question."

    target_path, start_hour, end_hour, target_day = params

    count = 0
    with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                log_time = match.group('time')
                request = match.group('request')
                status = int(match.group('status'))

                # Check conditions: correct weekday, time range, GET request, successful status, and path
                if is_valid_time(log_time, target_day, start_hour, end_hour):
                    request_parts = request.split()
                    if len(request_parts) >= 2 and request_parts[0] == "GET":
                        url = request_parts[1]
                        if url.startswith(f"/{target_path}/") and 200 <= status < 300:
                            count += 1

    return count


# Question 4
import re
import gzip
from collections import defaultdict
from datetime import datetime
# Regex pattern to parse Apache log entries
log_pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\S+) ".*?" ".*?"'
)
# Function to extract parameters from the question
def extract_params(question):
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", question)
    url_match = re.search(r"under\s+([a-zA-Z0-9_-]+)/", question)  # Extract URL prefix
    is_bottom = "bottom" in question.lower()  # Detect "bottom" keyword

    if date_match and url_match:
        target_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").strftime("%d/%b/%Y")
        url_prefix = f"/{url_match.group(1)}/"
        return target_date, url_prefix, is_bottom

    return None, None, None
# Function to find the top or bottom IP by data usage
def top_ip_data_usage(question, file_path):
    target_date, url_prefix, is_bottom = extract_params(question)

    if not target_date or not url_prefix:
        return {"answer": f"Invalid question format. Could not extract date or URL prefix from: {question}"}

    ip_bandwidth = defaultdict(int)  # Store total bytes downloaded per IP

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
            for line in file:
                match = log_pattern.match(line)
                if match:
                    ip = match.group('ip')
                    log_time = match.group('time')
                    request = match.group('request')
                    status = int(match.group('status'))
                    size = match.group('size')

                    # Convert "-" in size field to 0
                    size = int(size) if size.isdigit() else 0

                    # Check if request matches date and URL prefix
                    if target_date in log_time and 200 <= status < 300:
                        request_parts = request.split()
                        if len(request_parts) >= 2 and request_parts[1].startswith(url_prefix):
                            ip_bandwidth[ip] += size  # Aggregate bytes per IP

        # Identify the correct IP based on top/bottom request
        if ip_bandwidth:
            selected_ip = (
                min(ip_bandwidth, key=ip_bandwidth.get) if is_bottom else max(ip_bandwidth, key=ip_bandwidth.get)
            )
            selected_downloaded_bytes = ip_bandwidth[selected_ip]
            return str(int(selected_downloaded_bytes))
        else:
            return {"answer": "No matching requests found."}

    except Exception as e:
        return {"answer": f"Error processing file: {str(e)}"}


# Question 6
# import json

# def total_sales_value(question, file_path):
#     try:
#         total_sales = 0

#         # Read and parse JSONL file
#         with open(file_path, 'r', encoding='utf-8') as file:
#             for line in file:
#                 try:
#                     record = json.loads(line.strip())  # Load JSON object
#                     if "sales" in record and isinstance(record["sales"], (int, float)):  # Ensure valid numeric value
#                         total_sales += record["sales"]
#                 except json.JSONDecodeError:
#                     continue  # Skip invalid JSON lines

#         return {"answer": total_sales}

#     except Exception as e:
#         return {"answer": f"Error processing file: {str(e)}"}
