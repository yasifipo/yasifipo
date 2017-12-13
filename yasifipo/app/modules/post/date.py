from datetime import datetime

def get_date(yaml, filename):
    if 'date' in yaml.keys():
        try:
            date =  datetime.strptime(str(yaml['date']), "%Y%m%d")
            in_key = True
            try:
                date_filename = datetime.strptime(str(filename[:8]), "%Y%m%d")
                in_filename = True
                return date, in_key, in_filename
            except:
                in_filename = False
                return date, in_key, in_filename
        except:
            in_key = False
            try:
                date_filename = datetime.strptime(str(filename[:8]), "%Y%m%d")
                in_filename = True
                return date_filename, in_key, in_filename
            except:
                in_filename = False
                return None, in_key, in_filename
    else:
        in_key = False
        try:
            date_filename = datetime.strptime(str(filename[:8]), "%Y%m%d")
            in_filename = True
            return date_filename, in_key, in_filename
        except:
            in_filename = False
            return None, in_key, in_filename
