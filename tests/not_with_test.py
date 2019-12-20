from src.spotlight.errors import NOT_WITH_ERROR
from .validator_test import ValidatorTest


class NotWithTest(ValidatorTest):
    def setUp(self):
        self.field1 = "test1"
        self.field2 = "test2"
        self.not_with_error = NOT_WITH_ERROR.format(
            field=self.field2, other=self.field1
        )
        self.rules = {"test2": "not_with:test1"}

    def test_not_with_rule_with_both_fields_expect_error(self):
        data = {"test1": "hello", "test2": "world"}
        expected = self.not_with_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field2)

        self.assertEqual(errs[0], expected)

    def test_not_with_rule_with_first_field_expect_no_error(self):
        data = {"test1": "hello"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field2)

        self.assertEqual(errs, expected)

    def test_not_with_rule_with_second_field_expect_no_error(self):
        data = {"test2": "world"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field2)

        self.assertEqual(errs, expected)
