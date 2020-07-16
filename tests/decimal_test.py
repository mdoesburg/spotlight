from decimal import Decimal

from src.spotlight.errors import DECIMAL_ERROR
from .validator_test import ValidatorTest


class DecimalTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.decimal_error = DECIMAL_ERROR.format(field=self.field)

    def test_decimal_rule_with_string_expect_error(self):
        rules = {"test": "decimal"}
        data = {"test": "test"}
        expected = self.decimal_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_decimal_rule_with_integer_expect_error(self):
        rules = {"test": "decimal"}
        data = {"test": 1}
        expected = self.decimal_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_decimal_rule_with_float_expect_error(self):
        rules = {"test": "decimal"}
        data = {"test": 1.0}
        expected = self.decimal_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_decimal_rule_with_ten_expect_no_error(self):
        rules = {"test": "decimal"}
        data = {"test": Decimal("10.0")}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_decimals_with_invalid_values_expect_false(self):
        invalid_decimals = [0, 1, "0", "1", -1.0, 1.4, [], {}, True, False, "test"]

        for invalid_decimal in invalid_decimals:
            actual = self.validator.valid_decimal(invalid_decimal)
            self.assertEqual(actual, False)

    def test_valid_decimals_with_valid_values_expect_true(self):
        valid_decimals = [Decimal("-1.2"), Decimal("1.2"), Decimal("1"), Decimal("100")]

        for valid_decimal in valid_decimals:
            actual = self.validator.valid_decimal(valid_decimal)
            self.assertEqual(actual, True)
