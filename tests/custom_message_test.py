from src.spotlight.errors import MIN_STRING_ERROR, IN_ERROR, REQUIRED_IF_ERROR
from .validator_test import ValidatorTest


class CustomMessageTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_custom_rule_message_expect_new_message(self):
        rules = {"some_field": "email"}
        data = {"some_field": "this.is.not.a.valid.email"}
        new_message = "You've supplied an invalid e-mail address."
        self.validator.overwrite_messages = {"email": new_message}

        errors = self.validator.validate(data, rules)
        errs = errors.get("some_field")

        self.assertEqual(errs[0], new_message)

    def test_custom_field_rule_message_expect_new_message(self):
        rules = {"some_field": "required"}
        data = {}
        new_message = "Hey! This is a required field!"
        self.validator.overwrite_messages = {"some_field.required": new_message}

        errors = self.validator.validate(data, rules)
        errs = errors.get("some_field")

        self.assertEqual(errs[0], new_message)

    def test_custom_field_rule_message_with_field_param_expect_new_message(self):
        field = "some_field"
        rules = {"some_field": "required"}
        data = {}
        new_message = "Hey! The {field} field is a required field!"
        self.validator.overwrite_messages = {"some_field.required": new_message}

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], new_message.format(field=field))

    def test_custom_field_rule_message_with_min_param_expect_new_message(self):
        field = "some_field"
        rules = {"some_field": "min:5"}
        data = {"some_field": "oops"}
        new_message = "Hey! The {field} field has to be at least {min} chars!"
        self.validator.overwrite_messages = {"some_field.min": new_message}

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], new_message.format(field=field, min=5))

    def test_custom_field_expect_new_field(self):
        rules = {"some_field": "min:5"}
        data = {"some_field": "oops"}
        self.validator.overwrite_fields = {"some_field": "custom"}
        expected = MIN_STRING_ERROR.format(field="custom", min=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get("some_field")

        self.assertEqual(errs[0], expected)

    def test_custom_field_and_custom_other_field_expect_new_fields(self):
        rules = {"some_field1": "required", "some_field2": "required_with:some_field1"}
        data = {"some_field1": "hello"}
        new_message = "The {field} field has to be present with {other}."
        self.validator.overwrite_messages = {"some_field2.required_with": new_message}
        self.validator.overwrite_fields = {
            "some_field1": "custom1",
            "some_field2": "custom2",
        }
        expected = new_message.format(field="custom2", other="custom1")

        errors = self.validator.validate(data, rules)
        errs = errors.get("some_field2")

        self.assertEqual(errs[0], expected)

    def test_custom_field_message_with_custom_field_expect_new_message(self):
        rules = {"email": "email"}
        data = {"email": "this.is.not.a.valid.email"}
        new_message = "You've supplied an invalid {field}."
        self.validator.overwrite_messages = {"email": new_message}
        self.validator.overwrite_fields = {"email": "e-mail address"}
        expected = new_message.format(field="e-mail address")

        errors = self.validator.validate(data, rules)
        errs = errors.get("email")

        self.assertEqual(errs[0], expected)

    def test_custom_field_values_expect_errors_with_new_values(self):
        field = "some_field"
        new_values = "new1, new2, new3"
        rules = {"some_field": "in:val1,val2,val3"}
        data = {"some_field": "this.is.not.a.valid.email"}
        self.validator.overwrite_values = {
            "some_field": {"val1": "new1", "val2": "new2", "val3": "new3"}
        }
        expected = IN_ERROR.format(field=field, values=new_values)

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_custom_global_values_expect_errors_with_new_values(self):
        rules = {"field1": "in:crypto,cc,ideal", "field2": "in:crypto,cc,ideal"}
        data = {"field1": "test", "field2": "test"}
        self.validator.overwrite_values = {"cc": "credit card"}
        values = "crypto, credit card, ideal"

        errors = self.validator.validate(data, rules, flat=True)

        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0], IN_ERROR.format(field="field1", values=values))
        self.assertEqual(errors[1], IN_ERROR.format(field="field2", values=values))

    def test_custom_field_value_expect_error_with_new_value(self):
        rules = {"test": "required_if:other_field,cc"}
        data = {"other_field": "cc"}
        self.validator.overwrite_values = {"test": {"cc": "credit card"}}
        expected = REQUIRED_IF_ERROR.format(
            field="test", other="other_field", value="credit card"
        )

        errors = self.validator.validate(data, rules, flat=True)
        actual = errors[0]

        self.assertEqual(actual, expected)

    def test_custom_other_field_value_expect_error_with_new_value(self):
        rules = {
            "payment_type": "in:crypto,cc,ideal",
            "credit_card_number": "required_if:payment_type,cc",
        }
        data = {"payment_type": "cc"}
        self.validator.overwrite_values = {"payment_type": {"cc": "credit card"}}
        expected = REQUIRED_IF_ERROR.format(
            field="credit_card_number", other="payment_type", value="credit card"
        )

        errors = self.validator.validate(data, rules, flat=True)
        actual = errors[0]

        self.assertEqual(actual, expected)

    def test_custom_message_and_fields_and_value_expect_custom_error(self):
        new_message = "The {field} field is required when the {other} is {value}."
        field = "credit card number"
        other = "payment type"
        value = "credit card"

        rules = {
            "payment_type": "in:crypto,cc,ideal",
            "credit_card_number": "required_if:payment_type,cc",
        }
        data = {"payment_type": "cc"}

        self.validator.overwrite_messages = {
            "credit_card_number.required_if": new_message
        }
        self.validator.overwrite_fields = {
            "payment_type": other,
            "credit_card_number": field,
        }
        self.validator.overwrite_values = {"cc": value}
        expected = new_message.format(field=field, other=other, value=value)

        errors = self.validator.validate(data, rules)
        errs = errors.get("credit_card_number")

        self.assertEqual(expected, errs[0])
