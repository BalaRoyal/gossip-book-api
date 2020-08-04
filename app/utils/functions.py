import uuid
import os


def profile_image_upload_path(instance, filename):
    """Generate image upload path

    Args:
        instance (File): image file to upload
        filename (string): image file name
    """

    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join('uploads/profile_images/', filename)


def post_image_upload_path(instance, filename):
    """Generate image upload path

    Args:
        instance (File): image file to upload
        filename (string): image file name
    """

    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join('uploads/post_images/', filename)
