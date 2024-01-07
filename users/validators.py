import os
import string
from django.core.exceptions import ValidationError



def check_alphanum(value):
        if not any (c in string.ascii_letters for c in value) or not any(c in string.digits for c in value):
            raise ValidationError('Username must be alphanumeric. i.e It must contain letters and numbers.')

def validate_profile_image_extension(value):
    # Custom validator to allow only specific file extensions
    valid_extensions = ['.png', '.jpeg', '.jpg', '.svg']
    ext = os.path.splitext(value.name)[1].lower()  # Get the file extension
    if not ext in valid_extensions:
        raise ValidationError('Unsupported file extension. Only PNG, JPEG, and SVG are allowed.')