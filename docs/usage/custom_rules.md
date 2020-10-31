# Custom Rules

To create a new rule, create a class that inherits from the Rule class. A rule is required to have the following specifications:

- A rule should have a name attribute.
- A rule should implement the passes() method which contains the logic that determines if a value passes the rule.
- A rule should have a message property.

Here is an example of an uppercase rule:
```python
from spotlight import Rule


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