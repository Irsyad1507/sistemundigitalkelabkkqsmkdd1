import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_gambar_to_cloudinary(file, folder="calon"):
    """
    Upload image file to Cloudinary

    Args:
        file: Flask file object from request.files
        folder: Cloudinary folder name (default: "calon")

    Returns:
        dict with 'url' and 'public_id', or None if upload fails
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=f"sistemundigital/{folder}",
            resource_type="auto",
            quality="auto",
            fetch_format="auto",
        )
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
        }
    except Exception as e:
        print(f"Cloudinary upload error: {str(e)}")
        return None


def delete_gambar_from_cloudinary(public_id):
    """Delete image from Cloudinary by public_id"""
    try:
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        print(f"Cloudinary delete error: {str(e)}")
        return False
