from src.spotlight.errors import LIST_ERROR, REQUIRED_ERROR
from .validator_test import ValidatorTest


class ListTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.rules = {"test": "list"}
        self.list_error = LIST_ERROR.format(field=self.field)

    def test_list_rule_with_integer_expect_error(self):
        data = {"test": 1}
        expected = self.list_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_list_rule_with_list_expect_no_error(self):
        data = {"test": []}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_list_rule_and_required_with_empty_list_expect_error(self):
        rules = {"test": "required|list"}
        data = {"test": []}
        expected = REQUIRED_ERROR.format(field=self.field)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_list_rule_with_boolean_true_expect_error(self):
        data = {"test": True}
        expected = self.list_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_valid_list_with_dict_expect_false(self):
        actual = self.validator.valid_list(dict())

        self.assertEqual(actual, False)

    def test_valid_list_with_list_expect_true(self):
        actual = self.validator.valid_list([])

        self.assertEqual(actual, True)
