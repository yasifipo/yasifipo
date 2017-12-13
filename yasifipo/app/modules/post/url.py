from datetime import datetime
from .date import *

def url_mapping(yaml, filename, url):

    date, in_key, in_filename = get_date(yaml, filename)
    if date is None:
        return None

    url = url.replace('<year>', str(date.year))
    url = url.replace('<month>', str(date.month))
    url = url.replace('<day>', str(date.day))

    return url
