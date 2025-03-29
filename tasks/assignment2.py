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