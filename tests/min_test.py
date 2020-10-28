from decimal import Decimal

from src.spotlight.errors import MIN_STRING_ERROR, MIN_ERROR, MIN_ITEMS_ERROR
from .validator_test import ValidatorTest


class MinTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_min_rule_with_invalid_string_length_expect_error(self):
        rules = {"test": "min:5"}
        data = {"test": "1234"}
        expected = MIN_STRING_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_valid_string_length_expect_no_error(self):
        rules = {"test": "min:5"}
        data = {"test": "12345"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_min_rule_with_no_input_expect_no_error(self):
        rules = {"test": "min:5"}
        data = {}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_min_rule_with_empty_string_expect_error(self):
        rules = {"test": "min:5"}
        data = {"test": ""}
        expected = MIN_STRING_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_invalid_integer_expect_error(self):
        rules = {"test": "min:5"}
        data = {"test": 4}
        expected = MIN_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_invalid_float_expect_error(self):
        rules = {"test": "min:0.5"}
        data = {"test": 0.4}
        expected = MIN_ERROR.format(field=self.field, min=0.5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_invalid_decimal_expect_error(self):
        rules = {"test": "min:0.5"}
        data = {"test": Decimal("0.4")}
        expected = MIN_ERROR.format(field=self.field, min=0.5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_list_size_expect_error(self):
        rules = {"test": "min:5"}
        data = {"test": [1, 2, 3, 4]}
        expected = MIN_ITEMS_ERROR.format(field=self.field, min=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_int_value_and_float_rule_expect_error(self):
        rules = {"test": "min:1.1"}
        data = {"test": 1}
        expected = MIN_ERROR.format(field=self.field, min=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_min_rule_with_set_expect_error(self):
        rules = {"test": "min:1.1"}
        data = {"test": set()}
        expected = MIN_ERROR.format(field=self.field, min=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
