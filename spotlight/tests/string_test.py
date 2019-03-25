from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class StringTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.string_error = err.STRING_ERROR.format(field=self.field)

    def test_string_rule_with_integer_expect_error(self):
        rules = {
            "test": "string"
        }
        input_values = {
            "test": 1
        }
        expected = self.string_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_string_rule_with_string_expect_no_error(self):
        rules = {
            "test": "string"
        }
        input_values = {
            "test": "hello world"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_string_rule_with_boolean_false_expect_error(self):
        rules = {
            "test": "string"
        }
        input_values = {
            "test": False
        }
        expected = self.string_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_string_rule_with_boolean_true_expect_error(self):
        rules = {
            "test": "string"
        }
        input_values = {
            "test": True
        }
        expected = self.string_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
