import puremagic
from django.core.exceptions import ValidationError

def validate_pdf_only(file):

    file_head = file.read(2048)

    file.seek(0)

    try:
        
        matches = puremagic.from_string(file_head)

        if ".csv" not in matches:
            raise ValidationError("Incorrect file uploaded! Only csv files allowed")
        
    except puremagic.PureError:
        raise ValidationError("Could not identify file type")