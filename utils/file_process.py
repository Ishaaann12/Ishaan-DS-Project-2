import os
import tempfile
from fastapi import UploadFile
import gzip
import os
import tempfile
from fastapi import UploadFile
import io

def handle_file_processing(file: UploadFile) -> str:
    """Handles uploaded files without exceeding Vercel's memory limits."""
    if not file:
        print("📂 No file uploaded.")
        return None

    # Special handling for `.gz` files
    if file.filename.endswith(".gz"):
        try:
            print("📦 Processing .gz file directly from memory...")

            # Read the `.gz` file into memory (as a stream, without saving to disk)
            file.file.seek(0)  # Reset file pointer
            gz_stream = gzip.GzipFile(fileobj=io.BytesIO(file.file.read()), mode='rt', encoding='utf-8', errors='ignore')

            return gz_stream  # Return the stream (for processing functions)

        except Exception as e:
            print(f"❌ Error processing .gz file: {e}")
            return None

    else:
        # Standard processing for other files (saved to disk)
        temp_dir = tempfile.gettempdir()  # Get system temp directory (works on Vercel)
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as f:
            file.file.seek(0)  # Reset file pointer
            f.write(file.file.read())

        print(f"📦 File saved at {file_path} (standard processing)")
        return file_path  # Return the saved file path









# def handle_file_processing(file: UploadFile) -> str:
#     """Saves the uploaded file to a temporary directory and returns its path.
#        Special handling for `.gz` files to avoid memory issues.
#     """
#     if not file:
#         print("📂 No file uploaded.")
#         return None

#     # Use Vercel-compatible temporary storage
#     temp_dir = tempfile.gettempdir()  # Get system temp directory (works on Vercel)
#     file_path = os.path.join(temp_dir, file.filename)  # Save in /tmp/

#     try:
#         # Special handling for `.gz` files (processed in chunks)
#         if file.filename.endswith(".gz"):
#             with open(file_path, "wb") as f:
#                 for chunk in iter(lambda: file.file.read(1024 * 1024), b""):  # Read 1MB chunks
#                     f.write(chunk)
#             print(f"📦 .gz File saved at {file_path} (processed in chunks)")

#         else:
#             # Standard processing for all other files
#             with open(file_path, "wb") as f:
#                 file.file.seek(0)  # Reset file pointer
#                 f.write(file.file.read())

#             print(f"📦 File saved at {file_path} (standard processing)")

#         return file_path  # Return the saved file path

#     except Exception as e:
#         print(f"❌ Error saving file: {e}")
#         return None









# def handle_file_processing(file: UploadFile) -> str:
#     """Saves the uploaded file to a temporary directory and returns its path."""
#     if not file:
#         print("📂 No file uploaded.")
#         return None

#     # Use Vercel-compatible temporary storage
#     temp_dir = tempfile.gettempdir()  # Get system temp directory (works on Vercel)
#     file_path = os.path.join(temp_dir, file.filename)  # Save in /tmp/

#     # Save the file
#     with open(file_path, "wb") as f:
#         file.file.seek(0)  # Reset file pointer
#         f.write(file.file.read())

#     print(f"📦 File saved at {file_path}")
#     return file_path  # Return the saved file path



# import os
# from fastapi import UploadFile
# import tempfile
# def handle_file_processing(file: UploadFile) -> str:
#     """Saves the uploaded file to the current directory and returns its path."""
#     if not file:
#         print("📂 No file uploaded.")
#         return None

#     # Get the current directory
#     current_dir = os.getcwd()  # Current working directory
#     file_path = os.path.join(current_dir, file.filename)  # Full file path in the current directory

#     # Save the file to the current directory
#     with open(file_path, "wb") as f:
#         f.write(file.file.read())

#     print(f"📦 File saved at {file_path}")
#     return file_path  # Return the saved file path