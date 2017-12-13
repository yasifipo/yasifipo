from datetime import datetime
from .date import *

def url_mapping(date, yaml, filename, url):

    if date is None:
        return None

    url = url.replace('<year>', str(date.year))
    url = url.replace('<month>', str(date.month))
    url = url.replace('<day>', str(date.day))

    return url
