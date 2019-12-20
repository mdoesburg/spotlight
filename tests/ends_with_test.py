from src.spotlight.errors import ENDS_WITH_ERROR
from .validator_test import ValidatorTest


class EndsWithTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.in_error = ENDS_WITH_ERROR.format(
            field=self.field, values="val0, val1, val2"
        )

    def test_ends_with_rule_with_invalid_value_expect_error(self):
        data = {"test": "valueval3"}
        rules = {"test": "ends_with:val0,val1,val2"}
        expected = self.in_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_ends_with_rule_with_valid_value_expect_no_error(self):
        data = {"test": "valueval1"}
        rules = {"test": "ends_with:val0,val1,val2"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_ends_with_rule_with_valid_integer_expect_no_error(self):
        data = {"test": 5555555316}
        rules = {"test": "ends_with:111,316,743"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
