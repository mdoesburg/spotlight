from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class RequiredWithoutTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.required_without_error = err.REQUIRED_WITHOUT_ERROR.format(
            field=self.field,
            other=self.other_field
        )
        self.rules = {
            "test1": "",
            "test2": "required_without:test1"
        }

    def test_required_without_rule_with_missing_field_expect_error(self):
        input_values = {}
        expected = self.required_without_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_without_rule_with_field_present_expect_no_error(self):
        input_values = {
            "test2": "world"
        }
        expected = None

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
