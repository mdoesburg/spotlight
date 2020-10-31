# Validator

## Nested Validation
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

## List Validation

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

## Direct Validation

Sometimes there is a need for quick and simple validation, without having to create a rule set. The Validator class exposes several static methods that can be used for direct validation.

For example:

```python
validator = Validator()
email = "john.doe@example.com"

if validator.valid_email(email):
    print("This is a valid email!")
```

Or like this:
```python
if Validator.valid_email(email):
    print("This is a valid email!")
```

Available methods:

- valid_alpha_num
- valid_alpha_num_space
- valid_boolean
- valid_date_time
- valid_decimal
- valid_dict
- valid_email
- valid_float
- valid_integer
- valid_ip
- valid_json
- valid_list
- valid_string
- valid_url
- valid_uuid4