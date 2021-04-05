import uuid
from datetime import datetime 
from pzd_constants import DATE_FORMAT


def get_unique_id():
    return str(uuid.uuid4())

def datetime_to_str(date):
    return datetime.strftime(date, DATE_FORMAT)