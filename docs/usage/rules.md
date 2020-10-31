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
