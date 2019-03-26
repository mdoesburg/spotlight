from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class ListTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.rules = {
            "test": "list"
        }
        self.list_error = err.LIST_ERROR.format(field=self.field)

    def test_list_rule_with_integer_expect_error(self):
        input_values = {
            "test": 1
        }
        expected = self.list_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_list_rule_with_list_expect_no_error(self):
        input_values = {
            "test": []
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_list_rule_and_required_with_empty_list_expect_error(self):
        rules = {
            "test": "required|list"
        }
        input_values = {
            "test": []
        }
        expected = err.REQUIRED_ERROR.format(field=self.field)

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_list_rule_with_boolean_true_expect_error(self):
        input_values = {
            "test": True
        }
        expected = self.list_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
