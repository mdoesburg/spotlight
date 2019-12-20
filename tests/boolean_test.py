from src.spotlight.errors import BOOLEAN_ERROR
from .validator_test import ValidatorTest


class BooleanTest(ValidatorTest):
    def test_boolean_rule_with_invalid_values_expect_error(self):
        rules = {"test1": "boolean", "test2": "boolean"}
        data = {"test1": "test", "test2": 1}

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 2)
        for field, errs in errors.items():
            expected = BOOLEAN_ERROR.format(field=field)
            self.assertEqual(errs[0], expected)

    def test_boolean_rule_with_valid_values_expect_no_error(self):
        rules = {"test1": "boolean", "test2": "boolean"}
        data = {"test1": True, "test2": False}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_valid_boolean_with_invalid_values_expect_false(self):
        invalid_booleans = ["0", "1", -1, 0, 1, 2, [], {}]

        for invalid_boolean in invalid_booleans:
            actual = self.validator.valid_boolean(invalid_boolean)
            self.assertEqual(actual, False)

    def test_valid_boolean_with_valid_values_expect_true(self):
        valid_booleans = [True, False]

        for valid_boolean in valid_booleans:
            actual = self.validator.valid_boolean(valid_boolean)
            self.assertEqual(actual, True)
