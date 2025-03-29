import os
from fastapi import UploadFile
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