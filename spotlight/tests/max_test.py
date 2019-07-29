from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class MaxTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_max_rule_with_invalid_string_length_expect_error(self):
        rules = {
            "test": "max:5"
        }
        input_values = {
            "test": "123456"
        }
        expected = err.MAX_STRING_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_valid_string_length_expect_no_error(self):
        rules = {
            "test": "max:5"
        }
        input_values = {
            "test": "12345"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_max_rule_with_invalid_integer_expect_error(self):
        rules = {
            "test": "max:5"
        }
        input_values = {
            "test": 6
        }
        expected = err.MAX_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_invalid_float_expect_error(self):
        rules = {
            "test": "max:5.5"
        }
        input_values = {
            "test": 5.6
        }
        expected = err.MAX_ERROR.format(field=self.field, max=5.5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_list_size_expect_error(self):
        rules = {
            "test": "max:5"
        }
        input_values = {
            "test": [1, 2, 3, 4, 5, 6]
        }
        expected = err.MAX_LIST_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_none_expect_no_error(self):
        rules = {
            "test": "string|max:255"
        }
        input_values = {
            "test": None
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
