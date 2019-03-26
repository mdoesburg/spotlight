import json

from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class JsonTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.rules = {
            "test": "json"
        }
        self.json_error = err.JSON_ERROR.format(field=self.field)

    def test_json_rule_with_integer_expect_error(self):
        input_values = {
            "test": 1
        }
        expected = self.json_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_boolean_true_expect_error(self):
        input_values = {
            "test": True
        }
        expected = self.json_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_list_expect_error(self):
        input_values = {
            "test": []
        }
        expected = self.json_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_dict_expect_error(self):
        input_values = {
            "test": {}
        }
        expected = self.json_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_json_rule_with_json_string_expect_no_error(self):
        input_values = {
            "test": "{\"key\":\"value\"}"
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_json_rule_with_json_expect_no_error(self):
        data = dict()
        data["key"] = "value"
        json_data = json.dumps(data)
        input_values = {
            "test": json_data
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
