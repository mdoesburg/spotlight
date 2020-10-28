from decimal import Decimal

from src.spotlight.errors import SIZE_ERROR
from .validator_test import ValidatorTest


class SizeTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_size_rule_with_invalid_string_length_expect_error(self):
        rules = {"test": "size:5"}
        data = {"test": "1234"}
        expected = SIZE_ERROR.format(field=self.field, size=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_valid_string_length_expect_no_error(self):
        rules = {"test": "size:5"}
        data = {"test": "12345"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_size_rule_with_empty_string_expect_error(self):
        rules = {"test": "size:5"}
        data = {"test": ""}
        expected = SIZE_ERROR.format(field=self.field, size=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_invalid_integer_expect_error(self):
        rules = {"test": "size:5"}
        data = {"test": 4}
        expected = SIZE_ERROR.format(field=self.field, size=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_valid_integer_expect_no_error(self):
        rules = {"test": "size:5"}
        data = {"test": 5}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_size_rule_with_invalid_float_expect_error(self):
        rules = {"test": "size:0.5"}
        data = {"test": 0.4}
        expected = SIZE_ERROR.format(field=self.field, size=0.5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_valid_float_expect_no_error(self):
        rules = {"test": "size:0.5"}
        data = {"test": 0.5}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_size_rule_with_list_with_invalid_size_expect_error(self):
        rules = {"test": "size:5"}
        data = {"test": [1, 2, 3, 4]}
        expected = SIZE_ERROR.format(field=self.field, size=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_list_with_valid_size_expect_no_error(self):
        rules = {"test": "size:5"}
        data = {"test": [1, 2, 3, 4, 5]}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_size_rule_with_dict_with_invalid_size_expect_error(self):
        rules = {"test": "size:5"}
        data = {"test": {"test1": 1, "test2": 2, "test3": 3, "test4": 4}}
        expected = SIZE_ERROR.format(field=self.field, size=5)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_dict_with_valid_size_expect_no_error(self):
        rules = {"test": "size:5"}
        data = {"test": {"test1": 1, "test2": 2, "test3": 3, "test4": 4, "test5": 5}}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_size_rule_with_int_value_and_float_rule_expect_error(self):
        rules = {"test": "size:1.1"}
        data = {"test": 1}
        expected = SIZE_ERROR.format(field=self.field, size=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_decimal_value_with_valid_size_expect_no_error(self):
        rules = {"test": "size:5.2"}
        data = {"test": Decimal("5.2")}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_size_rule_with_decimal_value_with_invalid_size_expect_error(self):
        rules = {"test": "size:1.1"}
        data = {"test": Decimal("1.2")}
        expected = SIZE_ERROR.format(field=self.field, size=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_size_rule_with_set_expect_error(self):
        rules = {"test": "size:1.1"}
        data = {"test": set()}
        expected = SIZE_ERROR.format(field=self.field, size=1.1)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
