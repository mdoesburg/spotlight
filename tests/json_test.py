import json

from src.spotlight.errors import JSON_ERROR
from .validator_test import ValidatorTest


class JsonTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.rules = {"test": "json"}
        self.json_error = JSON_ERROR.format(field=self.field)

    def test_json_rule_with_integer_expect_error(self):
        data = {"test": 1}
        expected = self.json_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_boolean_true_expect_error(self):
        data = {"test": True}
        expected = self.json_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_list_expect_error(self):
        data = {"test": []}
        expected = self.json_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_dict_expect_error(self):
        data = {"test": {}}
        expected = self.json_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_json_string_expect_no_error(self):
        data = {"test": '{"key":"value"}'}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_json_rule_with_json_expect_no_error(self):
        json_data = json.dumps({"key": "values"})
        data = {"test": json_data}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_json_with_invalid_values_expect_false(self):
        values = [
            True,
            False,
            -1,
            0,
            1,
            2,
            [],
            {},
            "",
            set(),
            "test",
            "{invalid}",
            '{"invalid"}',
            '{"invalid":}',
            "{invalid: data}",
        ]

        for value in values:
            actual = self.validator.valid_json(value)
            self.assertEqual(actual, False)

    def test_valid_json_with_valid_values_expect_true(self):
        values = [
            json.dumps({"key": "values"}),
            bytearray('{"key": "values"}', "utf-8"),
            str.encode('{"key": "values"}'),
            bytes('{"key": "values"}', "utf-8"),
        ]

        for value in values:
            actual = self.validator.valid_json(value)
            self.assertEqual(actual, True)
