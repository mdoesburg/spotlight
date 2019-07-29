from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class FloatTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.float_error = err.FLOAT_ERROR.format(field=self.field)

    def test_float_rule_with_string_expect_error(self):
        rules = {
            "test": "float"
        }
        input_values = {
            "test": "test"
        }
        expected = self.float_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_float_rule_with_ten_expect_no_error(self):
        rules = {
            "test": "float"
        }
        input_values = {
            "test": 10.0
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_float_rule_with_boolean_false_expect_error(self):
        rules = {
            "test": "float"
        }
        input_values = {
            "test": False
        }
        expected = self.float_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_float_rule_with_boolean_true_expect_error(self):
        rules = {
            "test": "float"
        }
        input_values = {
            "test": True
        }
        expected = self.float_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_valid_float_with_string_expect_false(self):
        valid_float = self.validator.valid_float("invalid.float")

        self.assertEqual(valid_float, False)

    def test_valid_float_with_float_ten_expect_true(self):
        valid_float = self.validator.valid_float(10.0)

        self.assertEqual(valid_float, True)

    def test_valid_float_with_boolean_true_expect_false(self):
        valid_float = self.validator.valid_float(True)

        self.assertEqual(valid_float, False)

    def test_valid_float_with_boolean_false_expect_false(self):
        valid_float = self.validator.valid_float(False)

        self.assertEqual(valid_float, False)
