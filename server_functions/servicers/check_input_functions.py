from utils.imports import or_
from datetime import datetime




def check_is_valid_timestamp(timestamps):
    try:
        for timestamp in timestamps:
            datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False



def check_id_in_table(session, tables):
    for table in tables:
        if not session.query(table).filter(table.c['id'].in_([tables[table]])).count():
            return False, table
    return True, ''


def check_required_fields(request, fields):
    for i in fields:
       if not request.HasField(i):
            return False, i
    return True, ''


def check_string_fields(request, fields):
    for field_name in fields:
        field_value = getattr(request, field_name, None)
        if not field_value or not field_value.strip():
            return False, field_name
    return True, ''


def check_integer_fields(request, fields):
    for field_name in fields:
        field_value = getattr(request, field_name, None)
        if field_value < 0:
            return False, field_name
    return True, ''

def check_integer_in_range(field, int_range):
    if field not in int_range:
        return False, field
    return True, ''




def check_is_numeric_positive_list(values):
    try:
        for i in values:
            a = int(i)
            if a < 0:
                return False
        return True
    except:
        return False


def check_is_status_int_in_range(values):
    try:
        for i in values:
            a = int(i)
            if a not in (0, 1):
                return False
        return True
    except:
        return False


def check_string_is_not_empty(value):
    return value or value.strip()
