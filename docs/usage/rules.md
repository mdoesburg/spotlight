# Rules

## Definition

Validation rules can be defined in multiple ways.

### String Notation

You can write rules as single pipe delimited strings:

```python
rules = {
    "id": "required|integer",
    "email": "required|email",
    "first_name": "required|string",
    "last_name": "required|string",
    "password": "required|min:8|max:255",
}
```

### List Notation

Alternatively to the string notation, rules can be specified as lists of rules:

```python
rules = {
    "id": ["required", "integer"],
    "email": ["required", "email"],
    "first_name": ["required", "string"],
    "last_name": ["required", "string"],
    "password": ["required", "min:8", "max:255"],
}
```

## Function as a Rule

If you require some more custom or complex validation logic than what is provided by the available rules, but you don't want to create a [custom rule](custom_rules.md), you can use a lambda expression or a function as a rule. 

The expression or function is expected to return a string if the validation fails, or `None` if it passes. The returned string is your custom error message.

!!! note
    You can only use a function as a rule when using the [list notation](#list-notation).

!!! tip
    Python functions return `None` by default, so in most cases you probably don't want to explicitly return `None`.

### Examples

An example using a lambda expression:

```python
rules = {
    "some_field": [
        "required",
        "integer",
        lambda field, value, validator: f"The {field} field has to be greater than 2." if value <= 2 else None,
    ],
}
```

An example using a function:

```python
def custom_validate(field, value, validator):
    if value <= 2:
        return  f"The {field} field has to be greater than 2."


rules = {
    "some_field": ["required", "integer", custom_validate],
}
```

### Provided Arguments

Both lambda expressions and functions will have access to the following keyword arguments:

- **field** -- name of the field under validation
- **value** -- value of the field under validation
- **validator** -- instance of the validator

!!! tip
    If you only need `value` in your function or expression, you can use `**kwargs` to omit the rest:
    
    ```python
    def custom_validate(value, **kwargs):
        if value <= 2:
            return  "Value has to be greater than 2."
    ```