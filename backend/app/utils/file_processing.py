import os
import uuid

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(file, folder):
    """Saves the uploaded file to the specified folder."""
    # Use absolute path for safety
    upload_folder = os.path.join(os.getcwd(), folder)
    
    # Ensure the directory exists
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder)  # Create directory if not exists
        except Exception as e:
            print(f"Error creating directory {upload_folder}: {e}")
            raise
    
    # Generate a unique filename to avoid conflicts
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(upload_folder, filename)

    print(f"Saving file to: {file_path}")  # Log the file path

    try:
        file.save(file_path)  # Save the file
    except Exception as e:
        print(f"Error saving file {filename}: {e}")
        raise

    return file_path
