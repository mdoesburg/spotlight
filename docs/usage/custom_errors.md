# Custom Errors

If needed, you can specify custom error messages to overwrite the default error messages.

## Messages

You can overwrite all messages for a specific rule. In the example below we are overwriting all 'required' error messages:

```python
validator.overwrite_messages = {
    "required": "Hey! This is a required field!"
}
```

You can overwrite all messages for a specific field. In the example below we are overwriting all the error messages for the 'first_name' field:

```python
validator.overwrite_messages = {
    "first_name": "Hey! This field contains an error!"
}
```

You can overwrite an error message for a specific rule of a specific field. In the example below we are overwriting the 'first_name.required' error message:

```python
validator.overwrite_messages = {
    "first_name.required": "Hey! This is a required field!"
}
```


## Fields

If you would like the 'field' portion of your validation message to be replaced with a custom field name, you may do so like this:

```python
validator.overwrite_fields = {
    "email": "e-mail address"
}
```

## Values

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
validator.overwrite_values = {
    "cc": "credit card"
}
```

Now if the validation rule fails it will produce the following message:

```
The credit_card_number field is required if the payment_type field equals credit card.
```