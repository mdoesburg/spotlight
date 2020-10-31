# Spotlight
Data validation for Python, inspired by the Laravel framework.

---

**Documentation**: coming soon

**Source Code**: <a href="https://github.com/mdoesburg/spotlight" target="_blank">https://github.com/mdoesburg/spotlight</a>

---

## Table of Contents
* [Installation](#installation)
* [Dependencies](#dependencies)
* [Usage](#usage)
  * [Simple Examples](#simple-examples)
  * [Direct Validation](#direct-validation)
* [Available Rules](#available-rules)
* [Advanced Usage](#advanced-usage)
  * [Custom Error Messages](#custom-error-messages)
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

### Simple Examples
```python
rules = {
    "email": "required|email",
    "first_name": "required|string|max:255",
    "last_name": "required|string|max:255",
    "password": "required|min:8|max:255"
}

data = {
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "test1234"
}

validator = Validator()
errors = validator.validate(data, rules)
```

Nested validation:
```python
rules = {
    "token": "required|string",
    "person.first_name": "required|string|max:255",
    "person.last_name": "required|string|max:255",
    "person.email": "required|email",
    "person.password": "required|min:8|max:255"
}

data = {
    "token": "test-token",
    "person": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "test1234"
    }
}

validator = Validator()
errors = validator.validate(data, rules)
```

List validation:
```python
rules = {
    "players": "required|list|min:2",
    "players.*.username": "required"
}

data = {
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
errors = validator.validate(data, rules)
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
* valid_decimal
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
* [decimal](#decimal)
* [dict](#dict)
* [email](#email)
* [ends_with](#ends_with)
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
* [regex](#regex)
* [required](#required)
* [required_if](#required_if)
* [required_unless](#required_unless)
* [required_with](#required_without)
* [required_without](#required_without)
* [size](#size)
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

### before
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

### decimal
The field under validation must be a decimal.
```
decimal
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

### ends_with
The field under validation must end with one of the given values.
```
ends_with:value,other,...
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

Note: Since version 2.0, True and False are considered valid integers, because bool is an instance of int in Python.


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
The field under validation must be less than or equal to the given maximum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
max:value
```

### min
The field under validation must be greater than or equal to the given minimum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
min:value
```

### not_with
The field under validation can't be present if the other specified field is present.
```
not_with:other
```


### regex

The field under validation must match the given regular expression. Internally, this rule uses the Python re.fullmatch() function.
```
regex:pattern
```

Note: When using the regex rule, it may be necessary to specify rules in a list instead of using pipe delimiters, especially if the regular expression contains a pipe character, like so:
```python
rules = {
    "some_field": ["required", "regex:a|b"]
}
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

### size
The field under validation must have a size matching the given value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
size:value
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
```python
validator = Validator()
validator.overwrite_messages = {
    "required": "Hey! This is a required field!"
}
```

You can overwrite all messages for a specific field. In the example below we are overwriting all the error messages for the 'first_name' field:
```python
validator = Validator()
validator.overwrite_messages = {
    "first_name": "Hey! This field contains an error!"
}
```

You can overwrite an error message for a specific rule of a specific field. In the example below we are overwriting the 'first_name.required' error message:
```python
validator = Validator()
validator.overwrite_messages = {
    "first_name.required": "Hey! This is a required field!"
}
```

**Fields**

If you would like the 'field' portion of your validation message to be replaced with a custom field name, you may do so like this:
```python
validator = Validator()
validator.overwrite_fields = {
    "email": "e-mail address"
}
```

**Values**

Sometimes you may need the 'value' portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the payment_type has a value of cc:
```python
rules = {
    "credit_card_number": "required_if:payment_type,cc"
}
```

If this validation rule fails, it will produce the following error message:
```
The credit_card_number field is required if the payment_type field equals cc.
```

Instead of displaying cc as the payment type value, you may specify a custom value:
```python
validator = Validator()
validator.overwrite_values = {
    "cc": "credit card"
}
```

Now if the validation rule fails it will produce the following message:
```
The credit_card_number field is required if the payment_type field equals credit card.
```

### Custom Rules
To create a new rule, create a class that inherits from the Rule class. A rule is required to have the following specifications:
- A rule should have a name attribute.
- A rule should implement the passes() method which contains the logic that determines if a value passes the rule.
- A rule should have a message property.

Here is an example of an uppercase rule:
```python
from spotlight.rules import Rule


class UppercaseRule(Rule):
    """Uppercase"""

    name = "uppercase"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return value.upper() == value

    @property
    def message(self) -> str:
        return "The {field} field must be uppercase."
```

As shown in the above example, the passes() method will receive the following arguments:

- **field** -- name of the field under validation
- **value** -- value of the field under validation
- **parameters** -- list of rule parameters
- **validator** -- instance of the validator

After creating a custom rule it has to be registered with the validator:
```python
from custom_rules import UppercaseRule

validator = Validator()
validator.register_rule(UppercaseRule())
```

After registering the rule, it can be used:
```python
rules = {
    "test": "uppercase"
}

data = {
    "test": "HELLO WORLD!"
}
```

In addition to the name attribute, a rule has 2 additional attributes which are set to "False" by default: implicit & stop. These attributes may be overwritten. 

**Implicit**

Setting implicit to "True" will cause the field under validation to be validated against the rule even if the field is not present. This is useful for rules such as "required".

**Stop**

Setting stop to "True" causes the validator to stop validating the rest of the rules specified for the current field if the current rule fails. 

**Message Fields**

If a rule contains a message property that contains keyword arguments (words surrounded by curly braces) like the one in the example below, the "message_fields" variable needs to be set in the passes method.
```python
@property
def message(self) -> str:
    return "The {field} field must be uppercase."
```

The "message_fields" variable can be set as shown in the example below. The keyword arguments in the message property will be replaced with the values from the "message_fields" dictionary.
```python
def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
    self.message_fields = dict(field=field)
```

## Plugins
### Spotlight SQLAlchemy
To use database rules such as **unique** and **exists** checkout the [Spotlight SQLAlchemy](https://github.com/mdoesburg/spotlight-sqlalchemy) plugin.
