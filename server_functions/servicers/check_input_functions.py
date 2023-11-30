from utils.imports import or_
from datetime import datetime


def validate_update_data(update_data, error_messages, update_data_dict):
    if update_data.HasField('name'):
        if not check_string_is_not_empty(update_data.name):
            error_messages.append(
                'Error: <name> values are empty or consist of whitespaces only.')
        else:
            update_data_dict["name"] = update_data.name

    # Validate other fields and add to update_data_dict as needed
    if update_data.HasField('data'):
        update_data_dict["data"] = update_data.data

    if update_data.HasField('status'):
        if not check_is_status_int_in_range([update_data.status]):
            error_messages.append(
                'Error: <status> values are not integers or are not in (0, 1).')
        else:
            update_data_dict["status"] = update_data.status

    if update_data.HasField('tags'):
        if not check_string_is_not_empty(update_data.tags):
            error_messages.append(
                'Error: <tags> values are empty or consist of whitespaces only.')
        else:
            update_data_dict["tags"] = update_data.tags

    if update_data.HasField('description'):
        if not check_string_is_not_empty(update_data.description):
            error_messages.append(
                'Error: <description> values are empty or consist of whitespaces only.')
        else:
            update_data_dict["description"] = update_data.description

    if update_data.HasField('radius'):
        if not check_is_numeric_positive_list([update_data.radius]):
            error_messages.append(
                'Error: some <radius> values are not integers or are negative.')
        else:
            update_data_dict["radius"] = update_data.radius

    if update_data.HasField('scale'):
        if not check_is_numeric_positive_list([update_data.scale]):
            error_messages.append(
                'Error: some <scale> values are not integers or are negative.')
        else:
            update_data_dict["scale"] = update_data.scale

    if update_data.HasField('processedByMemberId'):
        if not check_is_numeric_positive_list([update_data.processedByMemberId]):
            error_messages.append(
                'Error: some <processedByMemberId> values are not integers or are negative.')
        else:
            update_data_dict["processedByMemberId"] = update_data.processedByMemberId

    if not any(update_data_dict.values()):
        error_messages.append('Error: No parameters to update.')



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
