import puremagic
from django.core.exceptions import ValidationError
import os

def validate_csv_only(file):
    ext = os.path.splitext(file.name)[1]

    if ext.lower() != '.csv':
        raise ValidationError("File extension must be .csv")
    
    REQUIRED_HEADERS = (
        "IPV4_SRC_ADDR,L4_SRC_PORT,IPV4_DST_ADDR,L4_DST_PORT,"
        "PROTOCOL,L7_PROTO,IN_BYTES,OUT_BYTES,IN_PKTS,"
        "OUT_PKTS,TCP_FLAGS,FLOW_DURATION_MILLISECONDS"
    )

    try:
        file.seek(0)
        first_line = file.readline().decode('utf-8').strip()
        file.seek(0)

        if first_line.upper() != REQUIRED_HEADERS.upper():
            raise ValidationError("Incorrect file uploaded! Only csv files allowed")
        
    except puremagic.PureError:
        raise ValidationError("Could not identify file type")