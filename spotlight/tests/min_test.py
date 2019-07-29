from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class MinTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_min_rule_with_invalid_string_length_expect_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": "1234"
        }
        expected = err.MIN_STRING_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_valid_string_length_expect_no_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": "12345"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_min_rule_with_no_input_expect_no_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {}
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_min_rule_with_empty_string_expect_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": ""
        }
        expected = err.MIN_STRING_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_invalid_integer_expect_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": 4
        }
        expected = err.MIN_INTEGER_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_invalid_float_expect_error(self):
        rules = {
            "test": "min:0.5"
        }
        input_values = {
            "test": 0.4
        }
        expected = err.MIN_FLOAT_ERROR.format(field=self.field, min=0.5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_list_size_expect_error(self):
        rules = {
            "test": "min:5"
        }
        input_values = {
            "test": [1, 2, 3, 4]
        }
        expected = err.MIN_LIST_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
