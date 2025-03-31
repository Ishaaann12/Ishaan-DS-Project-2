# ASSIGNMENT 5
from utils.file_process import handle_file_processing  # ✅ Import in each task file

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
        return str(len(student_ids))

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

import gzip

def count_successful_requests(question, gz_stream):
    """
    Count successful GET requests from a .gz stream without storing it in memory.
    """
    params = extract_parameters(question)
    if not params:
        return "Error: Could not extract parameters from the question."

    target_path, start_hour, end_hour, target_day = params
    count = 0
    MAX_LINES = 500000  # Stop processing after this many lines

    try:
        for i, line in enumerate(gz_stream):
            if i > MAX_LINES:
                print("⚠️ File too large, stopping processing early")
                break

            match = log_pattern.match(line)
            if match:
                log_time = match.group('time')
                request = match.group('request')
                status = int(match.group('status'))

                if is_valid_time(log_time, target_day, start_hour, end_hour):
                    request_parts = request.split()
                    if len(request_parts) >= 2 and request_parts[0] == "GET":
                        url = request_parts[1]
                        if url.startswith(f"/{target_path}/") and 200 <= status < 300:
                            count += 1

        return count

    except Exception as e:
        return f"Error: {str(e)}"















# def count_successful_requests(question, file_path):
#     """
#     Count successful GET requests for a specified path on a given weekday within a time range.
#     Uses streaming to handle large files efficiently.
#     """
#     params = extract_parameters(question)
#     if not params:
#         return "Error: Could not extract parameters from the question."

#     target_path, start_hour, end_hour, target_day = params

#     count = 0
#     try:
#         with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
#             for line in file:
#                 match = log_pattern.match(line)
#                 if match:
#                     log_time = match.group('time')
#                     request = match.group('request')
#                     status = int(match.group('status'))

#                     if is_valid_time(log_time, target_day, start_hour, end_hour):
#                         request_parts = request.split()
#                         if len(request_parts) >= 2 and request_parts[0] == "GET":
#                             url = request_parts[1]
#                             if url.startswith(f"/{target_path}/") and 200 <= status < 300:
#                                 count += 1

#         return count

#     except MemoryError:
#         return "Error: File is too large to process on the server."
# def count_successful_requests(question, file_path):
#     """
#     Count successful GET requests for a specified path on a given weekday within a time range.
#     """
#     # Extract parameters dynamically from the question
#     params = extract_parameters(question)
#     if not params:
#         return "Error: Could not extract parameters from the question."

#     target_path, start_hour, end_hour, target_day = params

#     count = 0
#     with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
#         for line in file:
#             match = log_pattern.match(line)
#             if match:
#                 log_time = match.group('time')
#                 request = match.group('request')
#                 status = int(match.group('status'))

#                 # Check conditions: correct weekday, time range, GET request, successful status, and path
#                 if is_valid_time(log_time, target_day, start_hour, end_hour):
#                     request_parts = request.split()
#                     if len(request_parts) >= 2 and request_parts[0] == "GET":
#                         url = request_parts[1]
#                         if url.startswith(f"/{target_path}/") and 200 <= status < 300:
#                             count += 1

#     return count


# Question 4
import re
import gzip
import requests  # To download file from URL
from collections import defaultdict
from datetime import datetime
from io import BytesIO  # For handling uploaded files

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

# Function to process the `.gz` file (handles both URL and uploaded file)
def top_ip_data_usage(question, file_url=None, uploaded_file=None):
    target_date, url_prefix, is_bottom = extract_params(question)

    if not target_date or not url_prefix:
        return {"answer": f"Invalid question format. Could not extract date or URL prefix from: {question}"}

    ip_bandwidth = defaultdict(int)  # Store total bytes downloaded per IP

    try:
        if file_url:
            # Step 1: Download the file from URL
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Raise an error for failed requests
            file_stream = response.raw  # Use raw response as file stream
        elif uploaded_file:
            # Step 2: Handle uploaded file (already in memory)
            file_stream = BytesIO(uploaded_file.read())  # Convert to file-like object
        else:
            return {"answer": "No file provided. Please provide either a URL or an uploaded file."}

        # Step 3: Process the file as a Gzip stream
        with gzip.GzipFile(fileobj=file_stream, mode='rt', encoding='utf-8', errors='ignore') as file:
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
            return str(str(selected_downloaded_bytes))
        else:
            return {"answer": "No matching requests found."}

    except requests.exceptions.RequestException as e:
        return {"answer": f"Error downloading file: {str(e)}"}

    except Exception as e:
        return {"answer": f"Error processing file: {str(e)}"}




# import re
# import gzip
# from collections import defaultdict
# from datetime import datetime
# # Regex pattern to parse Apache log entries
# log_pattern = re.compile(
#     r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\S+) ".*?" ".*?"'
# )
# # Function to extract parameters from the question
# def extract_params(question):
#     date_match = re.search(r"(\d{4}-\d{2}-\d{2})", question)
#     url_match = re.search(r"under\s+([a-zA-Z0-9_-]+)/", question)  # Extract URL prefix
#     is_bottom = "bottom" in question.lower()  # Detect "bottom" keyword

#     if date_match and url_match:
#         target_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").strftime("%d/%b/%Y")
#         url_prefix = f"/{url_match.group(1)}/"
#         return target_date, url_prefix, is_bottom

#     return None, None, None
# # Function to find the top or bottom IP by data usage
# def top_ip_data_usage(question, file_path):
#     target_date, url_prefix, is_bottom = extract_params(question)

#     if not target_date or not url_prefix:
#         return {"answer": f"Invalid question format. Could not extract date or URL prefix from: {question}"}

#     ip_bandwidth = defaultdict(int)  # Store total bytes downloaded per IP

#     try:
#         with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
#             for line in file:
#                 match = log_pattern.match(line)
#                 if match:
#                     ip = match.group('ip')
#                     log_time = match.group('time')
#                     request = match.group('request')
#                     status = int(match.group('status'))
#                     size = match.group('size')

#                     # Convert "-" in size field to 0
#                     size = int(size) if size.isdigit() else 0

#                     # Check if request matches date and URL prefix
#                     if target_date in log_time and 200 <= status < 300:
#                         request_parts = request.split()
#                         if len(request_parts) >= 2 and request_parts[1].startswith(url_prefix):
#                             ip_bandwidth[ip] += size  # Aggregate bytes per IP

#         # Identify the correct IP based on top/bottom request
#         if ip_bandwidth:
#             selected_ip = (
#                 min(ip_bandwidth, key=ip_bandwidth.get) if is_bottom else max(ip_bandwidth, key=ip_bandwidth.get)
#             )
#             selected_downloaded_bytes = ip_bandwidth[selected_ip]
#             return str(int(selected_downloaded_bytes))
#         else:
#             return {"answer": "No matching requests found."}

#     except Exception as e:
#         return {"answer": f"Error processing file: {str(e)}"}