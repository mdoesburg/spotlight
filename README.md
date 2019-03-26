# Spotlight
Laravel style input validation for Python.

## Table of Contents
* [Installation](#installation)
* [Dependencies](#dependencies)
* [Usage](#usage)
  * [Simple Input Examples](#simple-input-examples)
  * [Database Rule Examples](#database-rule-examples)
  * [Direct Validation](#direct-validation)
* [Available Rules](#available-rules)
* [Advanced Usage](#advanced-usage)
  * [Overwriting Messages](#overwriting-messages)
  * [Custom Rules](#custom-rules)


## Dependencies
* [python >= 3.6.0](https://www.python.org/)
* [SQLAlchemy >= 1.3.1](https://pypi.org/project/SQLAlchemy/) (optional)
  * Only needed if you want to use the database dependent rules: unique and exists.

## Installation
Spotlight can be installed via pip:

```
pip install spotlight
```

## Usage
```
from spotlight.validator import Validator
```

### Simple Input Examples
```
rules = {
    "email": "required|email",
    "first_name": "required|string|max:255",
    "last_name": "required|string|max:255",
    "password": "required|min:8|max:255"
}

input = {
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "test1234"
}

validator = Validator()
errors = validator.validate(input, rules)
```

### Database Rule Examples
```
rules = {
    "id": "exists:user,id",
    "email": "unique:user,email"
}

input = {
    "id": 1,
    "email": "john.doe@example.com"
}

validator = Validator()
errors = validator.validate(input, rules)
```

### Direct Validation
Sometimes there is a need for quick and simple validation, without having to create a rule set. The Validator class exposes several static methods that can be used for direct validation.

For example:
```
email = "john.doe@example.com"

if validator.valid_email(email):
    print("This is a valid email!")

# Or like this:

if Validator.valid_email(email):
    print("This is a valid email!")
```
Available methods:
* valid_email
* valid_url
* valid_ip
* valid_uuid4
* valid_string
* valid_integer
* valid_boolean
* valid_json
* valid_alpha_num
* valid_alpha_num_space

## Available Rules
* [required](#required)
* [required_without](#required_without)
* [required_with](#required_without)
* [required_if](#required_if)
* [not_with](#not_with)
* [filled](#filled)
* [email](#email)
* [url](#url)
* [ip](#ip)
* [min](#min)
* [max](#max)
* in
* alpha_num
* alpha_num_space
* string
* integer
* boolean
* json
* uuid4
* [unique (database)](#unique-database)
* [exists (database)](#exists-database)

### required
The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:
* The value is _None_.
* The value is an empty string.
* The value is an empty list.
```
required
```
Default message:
```
The {field} field is required.
```

### required_without
The field under validation must be present and not empty when the other specified field is not present.
```
required_without:other
```
Default message:
```
The {field} field is required if the {other} field is absent.
```

### required_with
The field under validation must be present and not empty if the other specified field is present.
```
required_with:other
```
Default message:
```
The {field} field is required if the {other} field is present.
```

### required_if
The field under validation must be present and not empty if the other specified field equals a certain value.
```
required_if:other,value
```
Default message:
```
The {field} field is required if the {other} field equals {value}.
```

### not_with
The field under validation can't be present if the other specified field is present.
```
not_with:other
```
Default message:
```
The {field} field can't be present when the {other} field is present.
```

### filled
The field under validation must not be empty when it is present.
```
filled
```
Default message:
```
The {field} field must not be empty when it is present.
```

### email
The field under validation must be a valid email address.
```
email
```
Default message:
```
Invalid email address.
```

### url
The field under validation must be a valid URL.
```
url
```
Default message:
```
Invalid URL.
```

### ip
The field under validation must be an IP address.
```
url
```
Default message:
```
Invalid IP address.
```

### min
The field under validation must be greater than or equal to the given minimum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For a list, value corresponds to the length of the list.
```
min:value
```
Default message:
```
The {field} field has to be at least {min} characters.
```

### max
The field under validation must be less than or equal to the given maximum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For a list, value corresponds to the length of the list.
```
max:value
```
Default message:
```
The {field} field cannot be longer than {max} characters.
```

### unique (database)
The field under validation must be unique in a given database table. The last 4 fields (ignore column, ignore value, where column, where value) are optional.
```
unique:table,column
```
```
unique:table,column,ignoreColumn,ignoreValue
```
```
unique:table,column,ignoreColumn,ignoreValue,whereColumn,whereValue
```
```
unique:table,column,null,null,whereColumn,whereValue
```
### exists (database)
The field under validation must exist on a given database table. The last 2 fields (where column, where value) are optional.
```
exists:table,column
```
```
exists:table,column,whereColumn,whereValue
```

## Advanced Usage
### Overwriting Messages
Docs coming soon...

### Custom Rules
Docs coming soon...
