# Spotlight
Laravel style data validation for Python.

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

Examples:
```
validator = Validator()
email = "john.doe@example.com"

if validator.valid_email(email):
    print("This is a valid email!")

# Or like this:

if Validator.valid_email(email):
    print("This is a valid email!")
```

Available methods:
* valid_alpha_num
* valid_alpha_num_space
* valid_boolean
* valid_date_time
* valid_dict
* valid_email
* valid_float
* valid_integer
* valid_ip
* valid_json
* valid_list
* valid_string
* valid_url
* valid_uuid4

## Available Rules
* [accepted](#accepted)
* [after](#after)
* [alpha_num](#alpha_num)
* [alpha_num_space](#alpha_num_space)
* [before](#before)
* [boolean](#boolean)
* [date_time](#date_time)
* [dict](#dict)
* [email](#email)
* [filled](#filled)
* [float](#float)
* [in](#in)
* [integer](#integer)
* [ip](#ip)
* [json](#json)
* [list](#list)
* [max](#max)
* [min](#min)
* [not_with](#not_with)
* [required](#required)
* [required_if](#required_if)
* [required_unless](#required_unless)
* [required_with](#required_without)
* [required_without](#required_without)
* [starts_with](#starts_with)
* [string](#string)
* [url](#url)
* [uuid4](#uuid4)

### accepted
The field under validation must be yes, on, 1, or true. This is useful for validating "Terms of Service" acceptance.
```
accepted
```

### after
The field under validation must be a value after a given date/time. For more details about formatting see the [date_time](#date_time) rule.
```
after:2019-12-31 12:00:00
```
If the after rule is accompanied by the date_time rule, and a non default format is specified, the specified format will be assumed for the after rule as well:
```
date_time:%H:%M:%S|after:12:00:00
```
Instead of passing a date/time string to be evaluated by the `strptime` Python function, you may specify another field to compare against the date/time:
```
after:some_field
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

### Before
The field under validation must be a value before a given date/time. For more details about formatting see the [date_time](#date_time) rule.
```
before:2019-12-31 12:00:00
```
If the before rule is accompanied by the date_time rule, and a non default format is specified, the specified format will be assumed for the after rule as well:
```
date_time:%H:%M:%S|before:12:00:00
```
Instead of passing a date/time string to be evaluated by the `strptime` Python function, you may specify another field to compare against the date/time:
```
before:some_field
```

### boolean
The field under validation must be a boolean.
```
boolean
```

### date_time
The field under validation must be a valid date/time matching the "YYYY-MM-DD hh:mm:ss" format, or a custom specified format. For example, a field being validated with the following format "date_time:%m/%d/%Y" must match the "MM/DD/YYYY" format. The date/time validation uses the `strptime` Python function. For more info on valid formatting symbols check the following [Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).
```
date_time
```
```
date_time:format
```

### dict
The field under validation must be a dict.
```
dict
```

### email
The field under validation must be a valid email address.
```
email
```

### filled
The field under validation must not be empty when it is present.
```
filled
```

### float
The field under validation must be a float.
```
float
```

### in
The field under validation must be included in the given list of values. 
```
in:value,other,...
```

### integer
The field under validation must be an integer.
```
integer
```

### ip
The field under validation must be an IP address.
```
ip
```

### json
The field under validation must be a valid JSON string.
```
json
```

### list
The field under validation must be a list.
```
list
```

### max
The field under validation must be less than or equal to the given maximum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For a list, value corresponds to the length of the list.
```
max:value
```

### min
The field under validation must be greater than or equal to the given minimum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For a list, value corresponds to the length of the list.
```
min:value
```

### not_with
The field under validation can't be present if the other specified field is present.
```
not_with:other
```

### required
The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:
* The value is _None_.
* The value is an empty string.
* The value is an empty list.
```
required
```

### required_if
The field under validation must be present and not empty if the other specified field equals a certain value.
```
required_if:other,value
```

### required_unless
The field under validation must be present and not empty unless the other specified field equals a certain value.
```
required_unless:other,value
```

### required_with
The field under validation must be present and not empty only if any of the other specified fields are present.
```
required_with:field1,field2,...
```

### required_without
The field under validation must be present and not empty only when any of the other specified fields are not present.
```
required_without:field1,field2,...
```

### starts_with
The field under validation must start with one of the given values.
```
starts_with:value,other,...
```

### string
The field under validation must be a string.
```
string
```

### url
The field under validation must be a valid URL.
```
url
```

### uuid4
The field under validation must be a valid uuid (version 4).
```
uuid4
```

## Advanced Usage
### Custom Error Messages
If needed, you can specify custom error messages to overwrite the default error messages.

**Messages**

You can overwrite all messages for a specific rule. In the example below we are overwriting all 'required' error messages:
```
validator = Validator()
validator.overwrite_messages = {
    "required": "Hey! This is a required field!"
}
```

You can overwrite all messages for a specific field. In the example below we are overwriting all the error messages for the 'first_name' field:
```
validator = Validator()
validator.overwrite_messages = {
    "first_name": "Hey! This field contains an error!"
}
```
You can overwrite an error message for a specific rule of a specific field. In the example below we are overwriting the 'first_name.required' error message:
```
validator = Validator()
validator.overwrite_messages = {
    "first_name.required": "Hey! This is a required field!"
}
```

**Fields**

If you would like the 'field' portion of your validation message to be replaced with a custom field name, you may do so like this:
```
validator = Validator()
validator.overwrite_fields = {
    "email": "e-mail address"
}
```

**Values**

Sometimes you may need the 'value' portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the payment_type has a value of cc:
```
validator = Validator()
validator.overwrite_values = {
    "email": "e-mail address"
}
```

### Custom Rules
To create a new rule, create a class that inherits from the Rule class. A rule is required to have the following specifications:
- A rule should have a name attribute.
- A rule should implement the passes() method which contains the logic that determines if a value passes the rule.
- A rule should have the message property.
```
from spotlight.rules import Rule


class UppercaseRule(Rule):
    """Uppercase"""

    name = "uppercase"

    def passes(self, field: str, value: Any, rule_values: str, data: dict) -> bool:
        self.message_fields = dict(field=field)

        return value.upper() == value

    @property
    def message(self) -> str:
        return "The {field} field must be uppercase."
```

## Plugins
### Spotlight SQLAlchemy
To use database rules such as **unique** and **exists** checkout the [Spotlight SQLAlchemy](https://github.com/mdoesburg/spotlight-sqlalchemy) plugin.
