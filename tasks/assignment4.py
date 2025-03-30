import requests
from bs4 import BeautifulSoup
import re


# Question 3
def fetch_wikipedia_outline(question):
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
import datetime
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
import pdfplumber
import pandas as pd

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

    try:
        extracted_data = []
        
        # ✅ Extract tables using `pdfplumber`
        with pdfplumber.open(file_path) as pdf:
            for page_num in range(group_start, group_end + 1):  # Loop through required pages
                if page_num > len(pdf.pages):  # Prevent index error
                    break
                page = pdf.pages[page_num - 1]
                tables = page.extract_table()  # Extract table from the page

                if tables:
                    extracted_data.extend(tables)

        if not extracted_data:
            return {"error": "No tables found in the PDF"}

        # ✅ Convert extracted table data into a DataFrame
        df = pd.DataFrame(extracted_data)

        # ✅ Identify the row containing column headers dynamically
        header_row_idx = df[df.iloc[:, 0].str.contains("Maths", na=False)].index[0]
        df = df.iloc[header_row_idx:].reset_index(drop=True)

        # ✅ Rename columns based on detected headers
        df.columns = df.iloc[0]  # First row is header
        df = df[1:].reset_index(drop=True)

        # ✅ Convert relevant columns to numeric
        df[subject] = pd.to_numeric(df[subject], errors="coerce")
        df[filter_subject] = pd.to_numeric(df[filter_subject], errors="coerce")
        df.dropna(subset=[subject, filter_subject], inplace=True)

        # ✅ Apply filtering based on the extracted parameters
        if comparison in ["more", "at least"]:
            filtered_data = df[df[filter_subject] >= min_marks]
        else:  # "less" or "at most"
            filtered_data = df[df[filter_subject] <= min_marks]

        # ✅ Calculate total Maths marks
        total_marks = filtered_data[subject].sum()

        return str(int(total_marks))

    except Exception as e:
        return {"error": str(e)}

# import re
# import pandas as pd
# import camelot
# def calculate_total_marks(question, file_path):
#     """Extracts parameters from the question and calculates total marks from a PDF file."""
    
#     print(f"📌 Received Question: {repr(question)}")  # Debugging print
#     print(f"🔎 Words in Question: {question.split()}")  # Word-by-word check

#     # 🔍 Updated regex (more flexible)
#     pattern = r"total\s+(\w+)\s+marks.*?(\d+)\s+(?:or\s+)?(more|less|at\s+least|at\s+most)?\s*marks\s+in\s+(\w+).*?groups\s+(\d+)-(\d+)"

#     match = re.search(pattern, question, re.IGNORECASE)

#     if not match:
#         print("❌ Regex match failed! (Possible extra spaces or incorrect format)")
#         return {"error": "Invalid question format"}

#     # Extract parameters
#     subject = match.group(1).capitalize()    # e.g., "Maths"
#     min_marks = int(match.group(2))          # e.g., 10
#     comparison = match.group(3) if match.group(3) else "more"  # Default to "more"
#     filter_subject = match.group(4).capitalize()  # e.g., "Biology"
#     group_start = int(match.group(5))        # e.g., 59
#     group_end = int(match.group(6))          # e.g., 83

#     print(f"✅ Extracted Parameters: {subject}, {min_marks} ({comparison}), {filter_subject}, Groups {group_start}-{group_end}")

#         # ✅ Convert groups to PDF page numbers dynamically
#     page_start = group_start  # Assuming 1 group = 1 page
#     page_end = group_end
#     pages = f"{page_start}-{page_end}"

#     print(f"✅ Extracted Parameters: {subject}, {min_marks} ({comparison}), {filter_subject}, Pages {pages}")

#     try:
#         # ✅ Extract tables from the relevant pages
#         tables = camelot.read_pdf(file_path, pages=pages, flavor='stream')

#         if tables.n == 0:
#             return {"error": "No tables found in the PDF"}

#         # ✅ Combine all extracted tables
#         df_list = [table.df for table in tables]
#         combined_df = pd.concat(df_list, ignore_index=True)

#         # ✅ Identify the row containing column headers dynamically
#         header_row_idx = combined_df[combined_df.iloc[:, 0] == "Maths"].index[0]
#         data = combined_df.iloc[header_row_idx + 1:].reset_index(drop=True)

#         # ✅ Rename columns based on extracted header row
#         data.columns = ["Maths", "Physics", "English", "Economics", "Biology"]  # Adjust as needed

#         # ✅ Convert relevant columns to numeric
#         data[subject] = pd.to_numeric(data[subject], errors="coerce")
#         data[filter_subject] = pd.to_numeric(data[filter_subject], errors="coerce")
#         data.dropna(subset=[subject, filter_subject], inplace=True)

#         # ✅ Apply filtering based on the extracted parameters
#         if comparison in ["more", "at least", ]:
#             filtered_data = data[data[filter_subject] >= min_marks]
#         else:  # "less" or "at most"
#             filtered_data = data[data[filter_subject] <= min_marks]

#         # ✅ Calculate total Maths marks
#         total_marks = filtered_data[subject].sum()

#         return str(int(total_marks))

#     except Exception as e:
#         return {"error": str(e)}