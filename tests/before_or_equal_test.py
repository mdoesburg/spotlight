from src.spotlight.errors import BEFORE_OR_EQUAL_ERROR
from .validator_test import ValidatorTest


class BeforeOrEqualTest(ValidatorTest):
    def test_before_or_equal_rule_with_valid_values_expect_no_errors(self):
        rules = {
            "dt1": "date_time|before_or_equal:2019-08-24 16:48:00",
            "dt2": "date_time|before_or_equal:2019-08-24 16:28:00",
            "dt3": "date_time|before_or_equal:2019-08-24 16:28:01",
        }
        data = {
            "dt1": "2019-08-24 16:28:00",
            "dt2": "2019-08-24 16:28:00",
            "dt3": "2019-08-24 16:28:00",
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_or_equal_rule_with_value_and_invalid_time_expect_error(self):
        field = "dt1"
        rules = {"dt1": "date_time|before_or_equal:2019-08-24 16:00:00"}
        data = {"dt1": "2019-08-24 16:00:01"}
        expected = BEFORE_OR_EQUAL_ERROR.format(
            field=field, other="2019-08-24 16:00:00"
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_or_equal_rule_with_custom_format_and_valid_value_expect_no_error(
        self,
    ):
        rules = {
            "dt1": "date_time:%m/%d/%Y %H:%M:%S|before_or_equal:08/24/2019 16:47:00"
        }
        data = {"dt1": "08/24/2019 16:47:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
