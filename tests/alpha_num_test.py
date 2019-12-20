from src.spotlight.errors import ALPHA_NUM_ERROR
from .validator_test import ValidatorTest


class AlphaNumTest(ValidatorTest):
    def test_alpha_num_rule_with_invalid_values_expect_errors(self):
        rules = {
            "field1": "alpha_num",
            "field2": "alpha_num",
            "field3": "alpha_num",
            "field4": "alpha_num",
        }
        data = {
            "field1": "!@#$%^&*",
            "field2": "alpha-123",
            "field3": "alpha_123",
            "field4": "alpha 123",
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 4)
        for field, errs in errors.items():
            expected = ALPHA_NUM_ERROR.format(field=field)
            self.assertEqual(errs[0], expected)

    def test_alpha_num_rule_with_valid_values_expect_no_errors(self):
        rules = {"field1": "alpha_num", "field2": "alpha_num", "field3": "alpha_num"}
        data = {"field1": "test", "field2": "1", "field3": "alpha123"}
        expected = None

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 0)
        for field, errs in errors.items():
            self.assertEqual(errs, expected)

    def test_valid_alpha_num_with_invalid_values_expect_false(self):
        values = [
            "!@#$%^&*",
            "alpha-123",
            "alpha_123",
            "alpha 123",
            1,
            [],
            {},
            True,
            False,
        ]

        for value in values:
            actual = self.validator.valid_alpha_num(value)
            self.assertEqual(actual, False)

    def test_valid_alpha_num_with_valid_values_expect_true(self):
        values = ["test", "1", "alpha123"]

        for value in values:
            actual = self.validator.valid_alpha_num(value)
            self.assertEqual(actual, True)
