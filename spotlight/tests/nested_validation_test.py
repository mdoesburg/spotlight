from spotlight.tests.validator_test import ValidatorTest
from spotlight import errors as errs


class NestedValidationTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_nested_validation_expect_error(self):
        rules = {"nested": {"test": "max:5|email"}, "non_nested": "max:1"}
        input_values = {"nested": {"test": "123456"}, "non_nested": "12"}
        expected = {
            "nested.test": [
                errs.MAX_STRING_ERROR.format(field="test", max=5),
                errs.INVALID_EMAIL_ERROR,
            ],
            "non_nested": [errs.MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_double_nested_validation_expect_error(self):
        rules = {
            "nested": {"test": "max:5|email", "double_nested": {"test2": "max:2"}},
            "non_nested": "max:1",
        }
        input_values = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        expected = {
            "nested.test": [
                errs.MAX_STRING_ERROR.format(field="test", max=5),
                errs.INVALID_EMAIL_ERROR,
            ],
            "nested.double_nested.test2": [
                errs.MAX_STRING_ERROR.format(field="test2", max=2)
            ],
            "non_nested": [errs.MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_double_nested_validation_custom_message_expect_error(self):
        rules = {
            "nested": {"test": "max:5|email", "double_nested": {"test2": "max:2"}},
            "non_nested": "max:1",
        }
        input_values = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_message = "Hey! The {field} field has to be at least {max} chars!"
        messages = {"nested.double_nested.test2.max": new_message}
        expected = {
            "nested.test": [
                errs.MAX_STRING_ERROR.format(field="test", max=5),
                errs.INVALID_EMAIL_ERROR,
            ],
            "nested.double_nested.test2": [new_message.format(field="test2", max=2)],
            "non_nested": [errs.MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_double_nested_validation_custom_field_expect_error(self):
        rules = {
            "nested": {"test": "max:5|email", "double_nested": {"test2": "max:2"}},
            "non_nested": "max:1",
        }
        input_values = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        fields = {"test2": "custom"}
        expected = {
            "nested.double_nested.test2": [
                errs.MAX_STRING_ERROR.format(field="custom", max=2)
            ],
            "nested.test": [
                errs.MAX_STRING_ERROR.format(field="test", max=5),
                errs.INVALID_EMAIL_ERROR,
            ],
            "non_nested": [errs.MAX_STRING_ERROR.format(field="non_nested", max=1)]
        }
        self.validator.overwrite_fields = fields

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_double_nested_validation_with_new_values_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "double_nested": {"test2": "in:val1,val2,val3"},
            },
            "non_nested": "max:1",
        }
        input_values = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_values = "piet, henk, jan"
        values = {"nested.double_nested.test2": {"values": new_values}}
        expected = {
            "nested.double_nested.test2": [
                errs.IN_ERROR.format(field="test2", values=new_values)
            ],
            "nested.test": [
                errs.MAX_STRING_ERROR.format(field="test", max=5),
                errs.INVALID_EMAIL_ERROR,
            ],
            "non_nested": [errs.MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }
        self.validator.overwrite_values = values

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_nested_required_field_expect_error(self):
        rules = {"nested": {"test": "required"}}
        input_values = {"nested": {}}
        expected = {"nested.test": [errs.REQUIRED_ERROR.format(field="test")]}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_nested_required_expect_error(self):
        rules = {"nested": {"test": "max:5|email"}}
        input_values = {"nested": {"test": "123456"}}
        expected = {
            "nested.test": [
                    errs.MAX_STRING_ERROR.format(field="test", max=5),
                    errs.INVALID_EMAIL_ERROR,
                ]
        }

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_double_nested_validation_with_flat_expect_flat_error_list(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "double_nested": {"test2": "in:val1,val2,val3"},
            },
            "non_nested": "max:1",
        }
        input_values = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_values = "piet, henk, jan"
        values = {"nested.double_nested.test2": {"values": new_values}}
        expected = [
            errs.MAX_STRING_ERROR.format(field="test", max=5),
            errs.INVALID_EMAIL_ERROR,
            errs.IN_ERROR.format(field="test2", values=new_values),
            errs.MAX_STRING_ERROR.format(field="non_nested", max=1),
        ]
        self.validator.overwrite_values = values

        errors = self.validator.validate(input_values, rules, flat=True)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_optional_field_and_empty_dict_expect_no_error(self):
        rules = {"nested": {"test": "email"}}
        input_values = {"nested": {}}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_optional_field_and_input_none_expect_no_error(self):
        rules = {"nested": {"test": "email"}}
        input_values = {"nested": None}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_optional_field_and_no_input_expect_no_error(self):
        rules = {"nested": {"test": "email"}}
        input_values = {}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_nested_validation_with_filled_field_and_no_input_expect_error(self):
        rules = {"nested": {"test": "filled"}}
        input_values = {"nested": {"test": None}}
        expected = {"nested.test": [errs.FILLED_ERROR.format(field="test")]}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)
