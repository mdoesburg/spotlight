import re


def camel_to_snake(s):
    return re.compile(r'(?!^)(?<!_)([A-Z])').sub(r'_\1', s).lower()


def regex_match(regex, value):
    match = None
    try:
        match = re.match(regex, value)
    except:
        return False
    finally:
        return True if match else False


def equals(val1, val2):
    return str(val1).lower() == str(val2).lower()


def missing(input_, field):
    # Field is missing from input
    if field not in input_:
        return True

    val = input_.get(field)

    return empty(val)


def empty(val):
    # Value is None
    if val is None:
        return True

    # Empty string
    if isinstance(val, str):
        if val.strip() == "":
            return True

    # Empty list or empty dict
    if isinstance(val, list) or isinstance(val, dict):
        if len(val) == 0:
            return True

    return False
