from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class AlphaNumTest(ValidatorTest):
    def test_alpha_num_rule_with_invalid_alpha_num_values_expect_errors(self):
        rules = {
            "field1": "alpha_num",
            "field2": "alpha_num",
            "field3": "alpha_num",
            "field4": "alpha_num",
        }
        input_values = {
            "field1": "!@#$%^&*",
            "field2": "alpha-123",
            "field3": "alpha_123",
            "field4": "alpha 123"
        }

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(len(errors.items()), 4)
        for field, errs in errors.items():
            expected = err.ALPHA_NUM_ERROR.format(field=field)
            self.assertEqual(errs[0], expected)

    def test_alpha_num_rule_with_valid_alpha_num_values_expect_no_errors(self):
        rules = {
            "field1": "alpha_num",
            "field2": "alpha_num",
            "field3": "alpha_num"
        }
        input_values = {
            "field1": "test",
            "field2": "1",
            "field3": "alpha123"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(len(errors.items()), 0)
        for field, errs in errors.items():
            self.assertEqual(errs, expected)
