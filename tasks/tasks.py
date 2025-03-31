from utils.file_process import handle_file_processing  # ✅ Import in each task file

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

# from GA1 import handle_http_get, process_readme_task, process_google_sheets_formula,process_excel_formula,count_days_in_range,extract_csv_from_zip, sort_json_array, process_text_to_json_multicursors, process_zip_for_symbol_sum


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

# Lazy Load Assignment Modules
assignment_modules = {
    "assignment1": ["handle_http_get","process_readme_task","process_google_sheets_formula","process_excel_formula","count_days_in_range","extract_csv_from_zip","sort_json_array","process_text_to_json_multicursors","process_zip_for_symbol_sum","calculate_filtered_size","count_different_lines"],
    "assignment2": ["process_light_pixel_task"],
    "assignment3": ["task_assignment3"],
    "assignment4": ["fetch_wikipedia_outline","get_weather_forecast","using_nominatim_api","search_hn_latest","calculate_total_marks"],
    "assignment5": ["count_unique_students","count_successful_requests","top_ip_data_usage"]
}

TASK_MAPPING = {
    "https": "handle_http_get",
    "google sheets": "process_google_sheets_formula",
    "excel": "process_excel_formula",
    "multi-cursors": "process_text_to_json_multicursors",
    "bounding box": "using_nominatim_api",
    "hacker news post": "search_hn_latest",
    "including both groups": "calculate_total_marks"
}

task_groups = {
    "extract_csv_from_zip": {"zip", "csv", "answer column"},
    "count_days_in_range": {"date range", "how many"},
    "sort_json_array": {"sort", "json", "array"},
    "process_zip_for_symbol_sum": {"encodings", "UTF-8", "CP-1252"},
    "process_readme_task": {"sha256sum", "npx", " -y prettier"},
    "count_different_lines": {"zip", "same number of lines", "identical files"},
    "process_light_pixel_task": {"brightness", "number of pixels", "There is a mistake"},
    "fetch_wikipedia_outline": {"URL", "API endpoint","Markdown outline that exposes an API"},
    "search_hn_latest": {"Hacker News", "latest post", "topic", "points"},
    "count_successful_requests": {"successful", "GET requests", "for pages"},
    "top_ip_data_usage": {"Across all requests", "bytes", "volume of downloads"},
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

def handle_task(question: str, file: Optional[UploadFile] = None):
    file_path = None
    if file:
        file_path = handle_file_processing(file)

    normalized_question = question.lower().replace("-", "")  # Normalize the question for all checks

    print(f"📩 Received question: {question}")

    # **1️⃣ Exact Match Check**
    for keyword, function_name in TASK_MAPPING.items():
        if keyword in normalized_question:
            print(f"✅ Exact match found: {keyword}, calling {function_name}")
            return execute_function(function_name, question, file_path)

    # **2️⃣ Multi-Keyword Match Check**
    for function_name, keywords in task_groups.items():
        matched_keywords = [kw for kw in keywords if kw in normalized_question]
        if len(matched_keywords) >= 2:
            print(f"✅ Multi-keyword match found ({matched_keywords}), calling {function_name}")
            return execute_function(function_name, question, file_path)

    # **3️⃣ Embeddings-Based Fallback**
    print("🔍 No exact or multi-keyword match found. Trying embeddings...")
    best_match = get_best_match_using_embeddings(normalized_question)

    if best_match:
        print(f"✅ Embeddings match found, calling {best_match}")
        return execute_function(best_match, question, file_path)

    print("❌ No match found.")
    return {"error": "No matching task found."}

import importlib
import inspect
def execute_function(function_name, question, file_path):
    """Dynamically import the correct assignment file and execute the function"""
    for module_name, function_names in assignment_modules.items():
        try:
            # Correct way to dynamically import modules
            module = importlib.import_module(f"tasks.{module_name}")
            if function_name in function_names:
                function = getattr(module, function_name, None)
                if function:
                    print(f"✅ Function {function_name} found in {module_name}")
                    sig = inspect.signature(function)
                    return function(question, file_path) if "file_path" in sig.parameters else function(question)
        except ImportError as e:
            print(f"⚠️ ImportError: {e}")  # Debugging information
            continue

    print(f"⚠️ Function {function_name} not found in any assignment file.")
    return {"error": "Function not found."}



def get_best_match_using_embeddings(normalized_question):
    """Use embeddings to find the best matching function"""
    question_embedding = get_embedding(normalized_question)
    if question_embedding is None:
        print("⚠️ Error: Failed to get embedding for question.")
        return None

    best_match = None
    best_score = 0

    for task_name, desc in task_descriptions.items():
        desc_embedding = get_embedding(desc.lower().replace("-", ""))

        similarity = sum(a * b for a, b in zip(question_embedding, desc_embedding))

        if similarity > best_score:
            best_score = similarity
            best_match = task_name

    return best_match if best_score > 0.75 else None


