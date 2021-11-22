from src.spotlight.errors import AFTER_OR_EQUAL_ERROR
from .validator_test import ValidatorTest


class AfterOrEqualTest(ValidatorTest):
    def test_after_or_equal_rule_with_valid_values_expect_no_errors(self):
        rules = {
            "dt1": "date_time|after_or_equal:2019-08-24 16:28:00",
            "dt2": "date_time|after_or_equal:2019-08-24 16:28:00",
            "dt3": "date_time|after_or_equal:2019-08-24 16:28:00",
        }
        data = {
            "dt1": "2019-08-24 16:48:00",
            "dt2": "2019-08-24 16:28:00",
            "dt3": "2019-08-24 16:28:01",
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_or_equal_rule_with_value_and_invalid_time_expect_error(self):
        field = "dt1"
        rules = {"dt1": "date_time|after_or_equal:2019-08-24 16:00:00"}
        data = {"dt1": "2019-08-24 15:59:59"}
        expected = AFTER_OR_EQUAL_ERROR.format(field=field, other="2019-08-24 16:00:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_after_or_equal_rule_with_custom_format_and_valid_value_expect_no_error(
        self,
    ):
        rules = {
            "dt1": "date_time:%m/%d/%Y %H:%M:%S|after_or_equal:08/24/2019 16:47:00"
        }
        data = {"dt1": "08/24/2019 16:47:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
