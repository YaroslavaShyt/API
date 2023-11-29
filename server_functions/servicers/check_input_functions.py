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
