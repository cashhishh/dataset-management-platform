"""
File service for handling CSV uploads and storage.
"""
import os
import aiofiles
from typing import Optional
from fastapi import UploadFile
import logging
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

# Upload directory configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".csv"}


def ensure_upload_dir():
    """Create upload directory if it doesn't exist"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        logger.info(f"Created upload directory: {UPLOAD_DIR}")


def validate_file_extension(filename: str) -> bool:
    """Check if file has allowed extension"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str, user_id: int) -> str:
    """Generate unique filename to avoid conflicts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    # Sanitize filename
    safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_'))[:50]
    return f"{user_id}_{timestamp}_{safe_name}{ext}"


async def save_upload_file(file: UploadFile, user_id: int) -> tuple[str, str, int]:
    """
    Save uploaded file to disk.
    
    Args:
        file: FastAPI UploadFile object
        user_id: ID of the user uploading
    
    Returns:
        Tuple of (file_path, original_filename, file_size)
    
    Raises:
        ValueError: If file validation fails
    """
    logger.info(f"Saving upload file: {file.filename} for user {user_id}")
    
    # Validate extension
    if not validate_file_extension(file.filename):
        logger.error(f"Invalid file type: {file.filename}")
        raise ValueError(f"Invalid file type. Only CSV files are allowed.")
    
    ensure_upload_dir()
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename, user_id)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    logger.info(f"Generated unique filename: {unique_filename}")
    
    # Save file and calculate size
    file_size = 0
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(8192):  # Read in 8KB chunks
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    # Clean up partial file
                    await out_file.close()
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    logger.error(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
                    raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")
                await out_file.write(chunk)
        
        logger.info(f"✓ File saved successfully: {file_path} ({file_size} bytes)")
        return file_path, file.filename, file_size
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.error(f"Cleaned up partial file: {file_path}")
        logger.error(f"Error saving file: {e}")
        raise


def delete_file(file_path: str) -> bool:
    """
    Delete a file from disk.
    
    Args:
        file_path: Path to the file
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
        return False


def get_file_size(file_path: str) -> Optional[int]:
    """Get file size in bytes"""
    try:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
    return None
