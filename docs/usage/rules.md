# Rules

## Definition

Validation rules can be defined in multiple ways.

You can write rules as single pipe delimited strings:

```python
rules = {
    "id": "required|int",
    "email": "required|email",
    "first_name": "required|string",
    "last_name": "required|string",
    "password": "required|min:8|max:255",
}
```

Alternatively, rules can be specified as lists of rules:

```python
rules = {
    "id": ["required", "int"],
    "email": ["required", "email"],
    "first_name": ["required", "string"],
    "last_name": ["required", "string"],
    "password": ["required", "min:8", "max:255"],
}
```

## Custom Validation Functions

If you require some more custom or complex validation logic than what is provided by the available rules, but you don't want to create a custom rule, you can pass a lambda expression or a function instead of a rule. The expression or function is expected to return a string if the validation fails.

Note: This only works with the list notation.

Lambda expression example:

```python
rules = {
    "some_field": [
        "required",
        "integer",
        lambda field, value, validator: f"The {field} field has to be greater than 2." if value <= 2 else None,
    ],
}
```

Function example:

```python
def custom_validate(field, value, validator):
    if value <= 2:
        return  f"The {field} field has to be greater than 2."


rules = {
    "some_field": ["required", "integer", custom_validate],
}
```

Both lambda expressions and functions will have access to `field`, `value`, and `validator` as keyword arguments.

Lets say you only need `value` in your custom function. You can use `**kwargs` to omit the rest:

```python
def custom_validate(value, **kwargs):
    if value <= 2:
        return  "Value has to be greater than 2."
```