from src.spotlight.errors import ACCEPTED_ERROR
from .validator_test import ValidatorTest


class AcceptedTest(ValidatorTest):
    def test_accepted_rule_with_invalid_values_expect_error(self):
        rules = {
            "tos1": "accepted",
            "tos2": "accepted",
            "tos3": "accepted",
            "tos4": "accepted",
        }
        data = {"tos1": "off", "tos2": 2, "tos3": False, "tos4": "no"}
        expected = ACCEPTED_ERROR

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 4)
        for field, errs in errors.items():
            self.assertEqual(errs[0], expected.format(field=field))

    def test_accepted_rule_with_valid_values_expect_no_error(self):
        rules = {
            "tos1": "accepted",
            "tos2": "accepted",
            "tos3": "accepted",
            "tos4": "accepted",
        }
        data = {"tos1": "on", "tos2": 1, "tos3": True, "tos4": "yes"}
        expected = ACCEPTED_ERROR

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 0)
        for field, errs in errors.items():
            self.assertEqual(errs[0], expected.format(field=field))
