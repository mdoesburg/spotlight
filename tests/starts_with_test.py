from src.spotlight.errors import STARTS_WITH_ERROR
from .validator_test import ValidatorTest


class StartsWithTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.in_error = STARTS_WITH_ERROR.format(
            field=self.field, values="val0, val1, val2"
        )

    def test_starts_with_rule_with_invalid_value_expect_error(self):
        data = {"test": "val3value"}
        rules = {"test": "starts_with:val0,val1,val2"}
        expected = self.in_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_starts_with_rule_with_valid_value_expect_no_error(self):
        data = {"test": "val1value"}
        rules = {"test": "starts_with:val0,val1,val2"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_starts_with_rule_with_valid_integer_expect_no_error(self):
        data = {"test": 3165555555}
        rules = {"test": "starts_with:111,316,555"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
