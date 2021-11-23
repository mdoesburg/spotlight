from src.spotlight.errors import (
    MAX_STRING_ERROR,
    EMAIL_ERROR,
    FILLED_ERROR,
    IN_ERROR,
    REQUIRED_ERROR,
    MIN_STRING_ERROR,
)
from .validator_test import ValidatorTest


class NestedValidationTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_nested_validation_expect_error(self):
        rules = {"nested.test": "max:5|email", "non_nested": "max:1"}
        data = {"nested": {"test": "123456"}, "non_nested": "12"}
        expected = {
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_double_nested_validation_expect_error(self):
        rules = {
            "nested.test": "max:5|email",
            "nested.double_nested.test2": "max:2",
            "non_nested": "max:1",
        }
        data = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        expected = {
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ],
            "nested.double_nested.test2": [
                MAX_STRING_ERROR.format(field="nested.double_nested.test2", max=2)
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_double_nested_validation_custom_message_expect_error(self):
        rules = {
            "nested.test": "max:5|email",
            "nested.double_nested.test2": "max:2",
            "non_nested": "max:1",
        }
        data = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_message = "Hey! The {field} field has to be at least {max} chars!"
        expected = {
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ],
            "nested.double_nested.test2": [
                new_message.format(field="nested.double_nested.test2", max=2)
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }
        self.validator.overwrite_messages = {
            "nested.double_nested.test2.max": new_message
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_double_nested_validation_custom_field_expect_error(self):
        rules = {
            "nested.test": "max:5|email",
            "nested.double_nested.test2": "max:2",
            "non_nested": "max:1",
        }
        data = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        expected = {
            "nested.double_nested.test2": [
                MAX_STRING_ERROR.format(field="custom", max=2)
            ],
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }
        self.validator.overwrite_fields = {"nested.double_nested.test2": "custom"}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_double_nested_validation_with_new_values_expect_error(self):
        rules = {
            "nested.test": "max:5|email",
            "nested.double_nested.test2": "in:val1,val2,val3",
            "non_nested": "max:1",
        }
        data = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_values = "new1, new2, new3"
        expected = {
            "nested.double_nested.test2": [
                IN_ERROR.format(field="nested.double_nested.test2", values=new_values)
            ],
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=1)],
        }
        self.validator.overwrite_values = {
            "nested.double_nested.test2": {
                "val1": "new1",
                "val2": "new2",
                "val3": "new3",
            }
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_nested_required_field_expect_error(self):
        rules = {"nested.test": "required"}
        data = {"nested": {}}
        expected = {"nested.test": [REQUIRED_ERROR.format(field="nested.test")]}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_nested_field_expect_error(self):
        rules = {"nested.test": "max:5|email"}
        data = {"nested": {"test": "123456"}}
        expected = {
            "nested.test": [
                MAX_STRING_ERROR.format(field="nested.test", max=5),
                EMAIL_ERROR.format(field="nested.test"),
            ]
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_double_nested_validation_with_flat_expect_error_list(self):
        rules = {
            "nested.test": "max:5|email",
            "nested.double_nested.test2": "in:val1,val2,val3",
            "non_nested": "max:1",
        }
        data = {
            "nested": {"test": "123456", "double_nested": {"test2": "12222"}},
            "non_nested": "12",
        }
        new_values = "new1, new2, new3"
        expected = [
            MAX_STRING_ERROR.format(field="nested.test", max=5),
            EMAIL_ERROR.format(field="nested.test"),
            IN_ERROR.format(field="nested.double_nested.test2", values=new_values),
            MAX_STRING_ERROR.format(field="non_nested", max=1),
        ]
        self.validator.overwrite_values = {
            "nested.double_nested.test2": {
                "val1": "new1",
                "val2": "new2",
                "val3": "new3",
            }
        }

        errors = self.validator.validate(data, rules, flat=True)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_optional_field_and_empty_dict_expect_no_error(self):
        rules = {"nested.test": "email"}
        data = {"nested": {}}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_optional_field_and_input_none_expect_no_error(self):
        rules = {"nested.test": "email"}
        data = {"nested": None}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_optional_field_and_no_input_expect_no_error(self):
        rules = {"nested.test": "email"}
        data = {}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_filled_field_and_no_input_expect_error(self):
        rules = {"nested.test": "filled"}
        data = {"nested": {"test": None}}
        expected = {"nested.test": [FILLED_ERROR.format(field="nested.test")]}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_required_field_expect_no_error(self):
        rules = {"nested.test": "required"}
        data = {"nested": {"test": "test"}}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_list(self):
        rules = {
            "nested.list.*.test": "required|max:2",
            "nested.list.*.test2": "min:2",
            "non_nested": "max:2",
        }
        data = {
            "nested": {
                "list": [
                    {"test": "12", "test2": "1"},
                    {"test2": "1"},
                    {"test": "1234", "test2": "1"},
                ]
            },
            "non_nested": "test",
        }
        expected = {
            "nested.list.1.test": [REQUIRED_ERROR.format(field="nested.list.1.test")],
            "nested.list.2.test": [
                MAX_STRING_ERROR.format(field="nested.list.2.test", max=2)
            ],
            "nested.list.0.test2": [
                MIN_STRING_ERROR.format(field="nested.list.0.test2", min=2)
            ],
            "nested.list.1.test2": [
                MIN_STRING_ERROR.format(field="nested.list.1.test2", min=2)
            ],
            "nested.list.2.test2": [
                MIN_STRING_ERROR.format(field="nested.list.2.test2", min=2)
            ],
            "non_nested": [MAX_STRING_ERROR.format(field="non_nested", max=2)],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_nested_validation_with_date_and_format_field_lookup_expect_no_error(self):
        rules = {"data.field": "date_time:%d-%m-%Y|before_or_equal:05-12-1980"}
        data = {"data": {"field": "04-12-1980"}}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
