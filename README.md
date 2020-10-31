# Spotlight
Data validation for Python, inspired by the Laravel framework.

---

**Documentation**: <a href="https://mdoesburg.github.io/spotlight/" target="_blank">https://mdoesburg.github.io/spotlight/</a>

**Source Code**: <a href="https://github.com/mdoesburg/spotlight" target="_blank">https://github.com/mdoesburg/spotlight</a>

---

## Requirements
* [Python 3.6+](https://www.python.org/)

## Installation

Spotlight can be installed via pip:

```bash
pip install spotlight
```
## Example

To validate data, we start by defining validation rules for each field we want to validate. After that, we pass the data and the validation rules into the Validator's validate method. 

Lets have a look at a simple example:

```python
from spotlight import Validator


rules = {
    "id": "required|int",
    "email": "required|email",
    "first_name": "required|string",
    "last_name": "required|string",
    "password": "required|min:8|max:255",
}

data = {
    "id": 1,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "test",
}

validator = Validator()
errors = validator.validate(data, rules)
```

The validate method will return a dictionary of errors, if any occurred.

In the example above, the validate method will return the following errors:

```python
{"password": ["The password field has to be at least 8 characters."]}
```

Alternatively, validation rules may be specified as lists of rules instead of a single | delimited string:

```python
rules = {
    "id": ["required", "int"],
    "email": ["required", "email"],
    "first_name": ["required", "string"],
    "last_name": ["required", "string"],
    "password": ["required", "min:8", "max:255"],
}
```

The full documentation can be found [here](https://mdoesburg.github.io/spotlight/).
