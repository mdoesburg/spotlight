REQUIRED_ERROR = "The {field} field is required."
REQUIRED_WITHOUT_ERROR = (
    "The {field} field is required if the {other} field is absent."
)
REQUIRED_WITH_ERROR = (
    "The {field} field is required if the {other} field is present."
)
REQUIRED_IF_ERROR = (
    "The {field} field is required if the {other} field equals {value}."
)
NOT_WITH_ERROR = (
    "The {field} field can't be present when the {other} field is present."
)
FILLED_ERROR = "The {field} field must not be empty when it is present."
INVALID_EMAIL_ERROR = "Invalid email address."
INVALID_URL_ERROR = "Invalid URL."
INVALID_IP_ERROR = "Invalid IP address."

MIN_STRING_ERROR = "The {field} field has to be at least {min} characters."
MAX_STRING_ERROR = "The {field} field cannot be longer than {max} characters."
MIN_INTEGER_ERROR = "The {field} field has to have a minimum value of {min}."
MAX_INTEGER_ERROR = "The {field} field has to have a maximum value of {max}."
MIN_LIST_ERROR = "The length of the {field} field has to be at least {min}."
MAX_LIST_ERROR = "The length of the {field} field cannot be greater than {max}."

IN_ERROR = "The {field} field must be one of the following values: {values}."
ALPHA_NUM_ERROR = "The {field} field can only contain letters and numbers."
ALPHA_NUM_SPACE_ERROR = (
    "The {field} field can only contain letters, numbers and spaces."
)
STRING_ERROR = "The {field} field must be a string."
INTEGER_ERROR = "The {field} field must be an integer."
BOOLEAN_ERROR = "The {field} field must be a boolean."
UUID4_ERROR = "The {field} field must be a valid UUID."
JSON_ERROR = "The {field} field must be a valid JSON string."

UNIQUE_ERROR = "A record with this {field} already exists."
EXISTS_ERROR = "A record with this {field} does not exists."
EXISTS_WHERE_ERROR = (
    "A record with this {field} does not exists for the given {other}."
)

NO_SESSION_ERROR = (
    "The rule '{rule}' requires a session, but no session was given to the "
    "validator."
)
RULE_NOT_FOUND = "The '{rule}' rule doesn't exist"
