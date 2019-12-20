from src.spotlight.errors import FLOAT_ERROR
from .validator_test import ValidatorTest


class FloatTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.float_error = FLOAT_ERROR.format(field=self.field)

    def test_float_rule_with_string_expect_error(self):
        rules = {"test": "float"}
        data = {"test": "test"}
        expected = self.float_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_float_rule_with_ten_expect_no_error(self):
        rules = {"test": "float"}
        data = {"test": 10.0}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_float_with_invalid_values_expect_false(self):
        invalid_floats = ["0", "1", -1, 0, 1, 2, [], {}, True, False, "test"]

        for invalid_float in invalid_floats:
            actual = self.validator.valid_float(invalid_float)
            self.assertEqual(actual, False)

    def test_valid_float_with_valid_values_expect_true(self):
        valid_floats = [-1.0, 0.0, 1.0, 5.0, 10.0]

        for valid_float in valid_floats:
            actual = self.validator.valid_float(valid_float)
            self.assertEqual(actual, True)
