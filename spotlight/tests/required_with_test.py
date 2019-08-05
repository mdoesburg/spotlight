from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class RequiredWithTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.required_with_error = err.REQUIRED_WITH_ERROR.format(
            field=self.field,
            other=self.other_field
        )
        self.rules = {
            "test2": "required_with:test1"
        }

    def test_required_with_rule_with_missing_field_expect_error(self):
        input_values = {
            "test1": "hello"
        }
        expected = self.required_with_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_with_rule_with_field_present_expect_no_error(self):
        input_values = {
            "test1": "hello",
            "test2": "world"
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_boolean_true_expect_no_error(self):
        input_values = {
            "test1": True,
            "test2": "world"
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_boolean_false_expect_no_error(self):
        input_values = {
            "test1": False,
            "test2": "world"
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
