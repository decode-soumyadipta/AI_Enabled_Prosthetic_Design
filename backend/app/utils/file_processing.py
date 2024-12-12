import os
import uuid

# Constants
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "stl"}
MAX_FILE_SIZE_MB = 10  # Maximum file size in MB

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, folder):
    """
    Saves the uploaded file to the specified folder.
    - Validates file type and size before saving.
    - Generates a unique filename to avoid conflicts.
    """
    # Use absolute path for safety
    upload_folder = os.path.join(os.getcwd(), folder)

    # Ensure the directory exists
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder)  # Create directory if it doesn't exist
        except Exception as e:
            print(f"Error creating directory {upload_folder}: {e}")
            raise

    # Validate file extension
    if not allowed_file(file.filename):
        raise ValueError(f"Invalid file type. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}")

    # Validate file size
    file.seek(0, os.SEEK_END)  # Move to the end of the file to get its size
    file_size_mb = file.tell() / (1024 * 1024)  # Size in MB
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.")
    file.seek(0)  # Reset file pointer for reading

    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(upload_folder, filename)

    print(f"Saving file to: {file_path}")  # Log the file path

    try:
        file.save(file_path)  # Save the file
    except Exception as e:
        print(f"Error saving file {filename}: {e}")
        raise

    return file_path


def clean_uploads(folder, retain_count=10):
    """
    Cleans the upload folder by retaining only the most recent `retain_count` files.
    """
    upload_folder = os.path.join(os.getcwd(), folder)
    if not os.path.exists(upload_folder):
        print(f"Upload folder does not exist: {upload_folder}")
        return

    # Get all files in the folder sorted by modification time
    files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Remove older files
    for old_file in files[retain_count:]:
        try:
            print(f"Deleting old file: {old_file}")
            os.remove(old_file)
        except Exception as e:
            print(f"Error deleting file {old_file}: {e}")
