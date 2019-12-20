from src.spotlight.errors import FILLED_ERROR
from .validator_test import ValidatorTest


class FilledTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.filled_error = FILLED_ERROR.format(field=self.field)
        self.rules = {"test": "filled"}

    def test_filled_rule_with_empty_string_expect_error(self):
        data = {"test": ""}
        expected = self.filled_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_filled_rule_with_field_present_expect_no_error(self):
        data = {"test": "hello"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_filled_rule_with_boolean_false_expect_no_error(self):
        data = {"test": False}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_filled_rule_with_spaces_expect_error(self):
        data = {"test": "   "}
        expected = self.filled_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_filled_rule_with_none_expect_error(self):
        data = {"test": None}
        expected = self.filled_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_filled_rule_with_no_input_expect_no_error(self):
        data = {}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
