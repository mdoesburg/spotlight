from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class IntegerTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.integer_error = err.INTEGER_ERROR.format(field=self.field)

    def test_integer_rule_with_string_expect_error(self):
        rules = {
            "test": "integer"
        }
        input_values = {
            "test": "test"
        }
        expected = self.integer_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_integer_rule_with_ten_expect_no_error(self):
        rules = {
            "test": "integer"
        }
        input_values = {
            "test": 10
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_integer_rule_with_boolean_false_expect_error(self):
        rules = {
            "test": "integer"
        }
        input_values = {
            "test": False
        }
        expected = self.integer_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_integer_rule_with_boolean_true_expect_error(self):
        rules = {
            "test": "integer"
        }
        input_values = {
            "test": True
        }
        expected = self.integer_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_valid_integer_with_string_expect_false(self):
        valid_integer = self.validator.valid_integer("invalid.integer")

        self.assertEqual(valid_integer, False)

    def test_valid_integer_with_integer_ten_expect_true(self):
        valid_integer = self.validator.valid_integer(10)

        self.assertEqual(valid_integer, True)

    def test_valid_integer_with_boolean_true_expect_false(self):
        valid_integer = self.validator.valid_integer(True)

        self.assertEqual(valid_integer, False)

    def test_valid_integer_with_boolean_false_expect_false(self):
        valid_integer = self.validator.valid_integer(False)

        self.assertEqual(valid_integer, False)
