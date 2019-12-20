from src.spotlight.errors import (
    MAX_STRING_ERROR,
    MIN_STRING_ERROR,
    IN_ERROR,
    REQUIRED_ERROR,
)
from .validator_test import ValidatorTest


class ListValidationTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}
        self.rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        self.data = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }

    def test_list_validation_expect_error(self):
        expected = {
            "list.1.test": [MAX_STRING_ERROR.format(field="list.1.test", max=2)],
            "list.2.test": [MAX_STRING_ERROR.format(field="list.2.test", max=2)],
            "list.0.test2": [MIN_STRING_ERROR.format(field="list.0.test2", min=2)],
            "list.1.test2": [MIN_STRING_ERROR.format(field="list.1.test2", min=2)],
            "list.2.test2": [MIN_STRING_ERROR.format(field="list.2.test2", min=2)],
        }

        errors = self.validator.validate(self.data, self.rules)

        self.assertEqual(errors, expected)

    def test_list_validation_flat_expect_error(self):
        expected = [
            MAX_STRING_ERROR.format(field="list.1.test", max=2),
            MAX_STRING_ERROR.format(field="list.2.test", max=2),
            MIN_STRING_ERROR.format(field="list.0.test2", min=2),
            MIN_STRING_ERROR.format(field="list.1.test2", min=2),
            MIN_STRING_ERROR.format(field="list.2.test2", min=2),
        ]

        errors = self.validator.validate(self.data, self.rules, flat=True)

        self.assertEqual(errors, expected)

    def test_list_validation_expect_with_custom_message_error(self):
        new_message = "Hey! The {field} can't be greater than {max} chars!"
        expected = {
            "list.1.test": [new_message.format(field="list.1.test", max=2)],
            "list.2.test": [new_message.format(field="list.2.test", max=2)],
            "list.0.test2": [MIN_STRING_ERROR.format(field="list.0.test2", min=2)],
            "list.1.test2": [MIN_STRING_ERROR.format(field="list.1.test2", min=2)],
            "list.2.test2": [MIN_STRING_ERROR.format(field="list.2.test2", min=2)],
        }
        self.validator.overwrite_messages = {"list.*.test.max": new_message}

        errors = self.validator.validate(self.data, self.rules)

        self.assertEqual(errors, expected)

    def test_list_validation_expect_with_custom_fields_error(self):
        expected = {
            "list.1.test": [MAX_STRING_ERROR.format(field="list.1.test", max=2)],
            "list.2.test": [MAX_STRING_ERROR.format(field="list.2.test", max=2)],
            "list.0.test2": [MIN_STRING_ERROR.format(field="custom", min=2)],
            "list.1.test2": [MIN_STRING_ERROR.format(field="custom", min=2)],
            "list.2.test2": [MIN_STRING_ERROR.format(field="custom", min=2)],
        }
        self.validator.overwrite_fields = {"list.*.test2": "custom"}

        errors = self.validator.validate(self.data, self.rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_values_message_expect_error_with_new_values(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "in:val1,val2,val3"}
        new_values = "new1, new2, new3"
        expected = {
            "list.1.test": [MAX_STRING_ERROR.format(field="list.1.test", max=2)],
            "list.2.test": [MAX_STRING_ERROR.format(field="list.2.test", max=2)],
            "list.0.test2": [IN_ERROR.format(field="list.0.test2", values=new_values)],
            "list.1.test2": [IN_ERROR.format(field="list.1.test2", values=new_values)],
            "list.2.test2": [IN_ERROR.format(field="list.2.test2", values=new_values)],
        }
        self.validator.overwrite_values = {
            "list.*.test2": {"val1": "new1", "val2": "new2", "val3": "new3"}
        }

        errors = self.validator.validate(self.data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_required_expect_error(self):
        rules = {"list.*.test": "required|max:2", "list.*.test2": "min:2"}
        data = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.1.test": [REQUIRED_ERROR.format(field="list.1.test")],
            "list.2.test": [MAX_STRING_ERROR.format(field="list.2.test", max=2)],
            "list.0.test2": [MIN_STRING_ERROR.format(field="list.0.test2", min=2)],
            "list.1.test2": [MIN_STRING_ERROR.format(field="list.1.test2", min=2)],
            "list.2.test2": [MIN_STRING_ERROR.format(field="list.2.test2", min=2)],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_optional_field_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        data = {"list": [{}, {}, {}]}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_required_field_expect_error(self):
        rules = {"list.*.test": "required|max:2", "list.*.test2": "min:2"}
        data = {"list": [{}, {}, {}]}
        expected = {
            "list.0.test": [REQUIRED_ERROR.format(field="list.0.test")],
            "list.1.test": [REQUIRED_ERROR.format(field="list.1.test")],
            "list.2.test": [REQUIRED_ERROR.format(field="list.2.test")],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_nested_dict_expect_no_error(self):
        rules = {
            "players": "required|list|min:2",
            "hello": "required|dict",
            "hello.test": "required|string",
            "players.*.name": "required|min:3|max:25",
            "players.*.unit": "required|dict",
            "players.*.unit.name": "required|string|max:3",
        }
        data = {
            "hello": {"test": "some_value"},
            "players": [
                {"name": "Test 1", "unit": {"name": "hi"}},
                {"name": "Test 2", "unit": {"name": "hi"}},
            ],
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_empty_list_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        data = {"list": []}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_with_dict_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        data = {"list": {}}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_validation_without_key_expect_no_error(self):
        rules = {
            "start_at": "string|min:10",
            "end_at": "string|min:10",
            "ticket_universe.size": "integer",
            "ticket_universe.positions.*": "string",
        }
        data = {
            "start_at": "2017:03:22",
            "end_at": "2028:03:26",
            "ticket_universe": {
                "size": 99,
                "positions": ["fixed:A", "ranged:1:2", "binary", "alpha", "numeric"],
            },
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
