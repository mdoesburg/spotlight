# Spotlight
Laravel style input validation for Python.

## Table of Contents
* [Installation](#installation)
* [Dependencies](#dependencies)
* [Usage](#usage)
  * [Simple Input Examples](#simple-input-examples)
  * [Direct Validation](#direct-validation)
* [Available Rules](#available-rules)
* [Advanced Usage](#advanced-usage)
  * [Overwriting Messages](#overwriting-messages)
  * [Custom Rules](#custom-rules)
* [Plugins](#plugins)
  * [Spotlight SQLAlchemy](#spotlight-sqlalchemy)

## Installation
Spotlight can be installed via pip:

```
pip install spotlight
```

## Dependencies
* [python >= 3.6.0](https://www.python.org/)

## Usage
```python
from spotlight.validator import Validator
```

### Simple Input Examples
```python
rules = {
    "email": "required|email",
    "first_name": "required|string|max:255",
    "last_name": "required|string|max:255",
    "password": "required|min:8|max:255"
}

input_ = {
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "test1234"
}

validator = Validator()
errors = validator.validate(input_, rules)
```

Nested validation:
```python
rules = {
    "token": "required|string",
    "person": {
        "first_name": "required|string|max:255",
        "last_name": "required|string|max:255",
        "email": "required|email",
        "password": "required|min:8|max:255"
    }
}

input_ = {
    "token": "test-token",
    "person": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "test1234"
    }
}

validator = Validator()
errors = validator.validate(input_, rules)
```

List validation:
```python
rules = {
    "players": "required|list|min:2",
    "players.*.username": "required"
}

input_ = {
    "players": [
        {
            "username": "Player 1"
        },
        {
            "username": "Player 2"
        }
    ]
}

validator = Validator()
errors = validator.validate(input_, rules)
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
* valid_list
* valid_dict
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
* [in](#in)
* [alpha_num](#alpha_num)
* [alpha_num_space](#alpha_num_space)
* [string](#string)
* [integer](#integer)
* [boolean](#boolean)
* [list](#list)
* [dict](#dict)
* [json](#json)
* [uuid4](#uuid4)
* [accepted](#accepted)
* [starts_with](#starts_with)

### required
The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:
* The value is _None_.
* The value is an empty string.
* The value is an empty list.
```
required
```

### required_without
The field under validation must be present and not empty when the other specified field is not present.
```
required_without:other
```

### required_with
The field under validation must be present and not empty if the other specified field is present.
```
required_with:other
```

### required_if
The field under validation must be present and not empty if the other specified field equals a certain value.
```
required_if:other,value
```

### not_with
The field under validation can't be present if the other specified field is present.
```
not_with:other
```

### filled
The field under validation must not be empty when it is present.
```
filled
```

### email
The field under validation must be a valid email address.
```
email
```

### url
The field under validation must be a valid URL.
```
url
```

### ip
The field under validation must be an IP address.
```
url
```

### min
The field under validation must be greater than or equal to the given minimum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For a list, value corresponds to the length of the list.
```
min:value
```

### max
The field under validation must be less than or equal to the given maximum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For a list, value corresponds to the length of the list.
```
max:value
```

### in
The field under validation must be included in the given list of values. 
```
in:value,other,...
```

### alpha_num
The field under validation must be entirely alpha-numeric characters.
```
alpha_num
```

### alpha_num_space
The field under validation may have alpha-numeric characters, as well as spaces.
```
alpha_num_space
```

### string
The field under validation must be a string.
```
string
```

### integer
The field under validation must be an integer.
```
string
```

### boolean
The field under validation must be a boolean.
```
boolean
```

### list
The field under validation must be a list.
```
list
```

### dict
The field under validation must be a dict.
```
dict
```

### json
The field under validation must be a valid JSON string.
```
json
```

### uuid4
The field under validation must be a valid uuid (version 4).
```
uuid4
```

### accepted
The field under validation must be yes, on, 1, or true. This is useful for validating "Terms of Service" acceptance.
```
accepted
```

### starts_with
The field under validation must start with one of the given values.
```
starts_with:value,other,...
```

## Advanced Usage
### Overwriting Messages
Docs coming soon...

### Custom Rules
Docs coming soon...

## Plugins
### Spotlight SQLAlchemy
To use database rules such as **unique** and **exists** checkout the [Spotlight SQLAlchemy](https://github.com/mdoesburg/spotlight-sqlalchemy) plugin.
