from decimal import Decimal

from src.spotlight.errors import MAX_STRING_ERROR, MAX_ERROR, MAX_ITEMS_ERROR
from .validator_test import ValidatorTest


class MaxTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_max_rule_with_invalid_string_length_expect_error(self):
        rules = {"test": "max:5"}
        data = {"test": "123456"}
        expected = MAX_STRING_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_valid_string_length_expect_no_error(self):
        rules = {"test": "max:5"}
        data = {"test": "12345"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_max_rule_with_invalid_integer_expect_error(self):
        rules = {"test": "max:5"}
        data = {"test": 6}
        expected = MAX_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_invalid_decimal_expect_error(self):
        rules = {"test": "max:5"}
        data = {"test": Decimal("6")}
        expected = MAX_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_invalid_float_expect_error(self):
        rules = {"test": "max:5.5"}
        data = {"test": 5.6}
        expected = MAX_ERROR.format(field=self.field, max=5.5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_list_size_expect_error(self):
        rules = {"test": "max:5"}
        data = {"test": [1, 2, 3, 4, 5, 6]}
        expected = MAX_ITEMS_ERROR.format(field=self.field, max=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_max_rule_with_none_expect_no_error(self):
        rules = {"test": "string|max:255"}
        data = {"test": None}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_max_rule_with_set_expect_error(self):
        rules = {"test": "max:1.1"}
        data = {"test": set()}
        expected = MAX_ERROR.format(field=self.field, max=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
