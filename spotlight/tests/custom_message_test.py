from spotlight.tests.validator_test import ValidatorTest
from spotlight import errors as err


class CustomMessageTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_custom_field_message_expect_new_message(self):
        new_message = "You've supplied an invalid e-mail address."
        rules = {
            "email": "email"
        }
        input_values = {
            "email": "this.is.not.a.valid.email"
        }
        messages = {
            "email": new_message
        }
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("email")

        self.assertEqual(errs[0], new_message)

    def test_custom_subfield_message_expect_new_message(self):
        new_message = "Hey! This is a required field!"
        rules = {
            "email": "required"
        }
        input_values = {}
        messages = {
            "email.required": new_message
        }
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("email")

        self.assertEqual(errs[0], new_message)

    def test_custom_subfield_message_with_field_expect_new_message(self):
        new_message = "Hey! The {field} field is a required field!"
        rules = {
            "email": "required"
        }
        input_values = {}
        messages = {
            "email.required": new_message
        }
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("email")

        self.assertEqual(errs[0], new_message.format(field="email"))

    def test_custom_subfield_message_with_min_expect_new_message(self):
        new_message = "Hey! The {field} field has to be at least {min} chars!"
        rules = {
            "email": "min:5"
        }
        input_values = {
            "email": "oops"
        }
        messages = {
            "email.min": new_message
        }
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("email")

        self.assertEqual(errs[0], new_message.format(field="email", min=5))

    def test_custom_field_expect_new_field(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": "oops"
        }
        fields = {
            "test": "custom"
        }
        self.validator.overwrite_fields = fields
        expected = err.MIN_STRING_ERROR.format(field="custom", min=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("test")

        self.assertEqual(errs[0], expected)

    def test_custom_field_and_custom_other_field_expect_new_fields(self):
        new_message = "The {field} field has to be present with {other}."
        rules = {
            "test1": "required",
            "test2": "required_with:test1"
        }
        input_values = {
            "test1": "hello"
        }
        messages = {
            "test2.required_with": new_message
        }
        fields = {
            "test1": "custom",
            "test2": "lol"
        }
        self.validator.overwrite_messages = messages
        self.validator.overwrite_fields = fields
        expected = new_message.format(field="lol", other="custom")

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("test2")

        self.assertEqual(errs[0], expected)

    def test_custom_field_message_with_custom_field_expect_new_message(self):
        new_message = "You've supplied an invalid {field}."
        rules = {
            "email2": "email"
        }
        input_values = {
            "email2": "this.is.not.a.valid.email"
        }
        messages = {
            "email2": new_message
        }
        fields = {
            "email2": "e-mail address"
        }
        self.validator.overwrite_messages = messages
        self.validator.overwrite_fields = fields

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("email2")

        self.assertEqual(errs[0], new_message.format(field="e-mail address"))

    def test_custom_values_with_in_rule_expect_new_values(self):
        field = "test"
        new_values = "piet, henk, jan"
        rules = {
            "test": "in:val1,val2,val3"
        }
        input_values = {
            "test": "this.is.not.a.valid.email"
        }
        values = {
            "test": {
                "values": new_values
            }
        }
        self.validator.overwrite_values = values
        expected = err.IN_ERROR.format(field=field, values=new_values)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_custom_fields_with_required_if_rule_expect_new_fields(self):
        new_message = "The {field} field is required when {other} is {value}."
        field = "credit card number"
        other = "payment type"
        value = "credit card"
        rules = {
            "payment_type": "in:crypto,cc,ideal",
            "credit_card_number": "required_if:payment_type,cc"
        }
        input_values = {
            "payment_type": "cc"
        }
        messages = {
            "credit_card_number.required_if": new_message
        }
        fields = {
            "payment_type": other,
            "credit_card_number": field,
            "cc": value
        }
        self.validator.overwrite_messages = messages
        self.validator.overwrite_fields = fields
        expected = new_message.format(
            field=field,
            other=other,
            value=value
        )

        errors = self.validator.validate(input_values, rules)
        errs = errors.get("credit_card_number")

        self.assertEqual(expected, errs[0])
