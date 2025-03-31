print("assignment1.py loaded, handle_http_get defined")

from typing import Optional
import requests
from fastapi import UploadFile
from urllib.parse import urlencode
import re
import json
import os
import requests
from typing import Optional
from dotenv import load_dotenv
from fastapi import UploadFile
from utils.file_process import handle_file_processing  # ✅ Import in each task file

import zipfile
import pandas as pd
import tempfile
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


# Question 3
import subprocess
import shutil
import os
import traceback
import time
from fastapi import UploadFile
def check_npx():
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


# Question 4
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

        return str(int(count))

    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}


# Question 8
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

    
# Question 9
import json
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
import hashlib
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

    return json_hash


# Question 12
import zipfile
import tempfile
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
            return str(int(total_sum))

        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"answer": f"Error: {str(e)}"}


# Question 15
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
    # **Extract parameters dynamically from the question**
    min_size = extract_number(question)  # Extract file size
    min_date = extract_datetime(question)  # Extract date-time
    
    if min_size is None or min_date is None:
        return {"error": "Could not extract required parameters from the question."}
    
    # **Extract ZIP contents**
    extract_dir = "/tmp/extracted_files"
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


# Question 17
def count_different_lines(question, file_path):

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