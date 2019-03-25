# Python Validator
Laravel style input validation for Python.

## Installation
Python Validator can be installed via pip:

`pip install spotlight`

## Usage
```
from spotlight import Validator
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

### Unique & Exists Examples
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
More examples coming soon...

## Available Rules
* required
* required_without
* required_with
* required_if
* not_with
* filled
* email
* url
* ip
* min
* max
* in
* alpha_num
* alpha_num_space
* string
* integer
* boolean
* uuid4
* unique (database)
* exists (database)

## Custom Rules
Docs coming soon...