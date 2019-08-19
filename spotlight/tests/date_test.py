from spotlight.errors import DATE_ERROR
from spotlight.tests.validator_test import ValidatorTest


class DateTest(ValidatorTest):
    def test_date_rule_with_valid_values_expect_no_error(self):
        rules = {"date1": "date", "date2": "date"}
        data = {"date1": "2019-12-31", "date2": "2019-01-01"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_rule_with_invalid_value_expect_error(self):
        rules = {"date1": "date", "date2": "date"}
        data = {"date1": "", "date2": 102323}

        errors = self.validator.validate(data, rules)

        for field, field_errors in errors.items():
            expected = DATE_ERROR.format(field=field)
            self.assertEqual(field_errors[0], expected)

    def test_valid_date_with_valid_values_expect_true(self):
        values = ["2019-12-31", "2019-01-01"]

        for value in values:
            actual = self.validator.valid_date(value)
            self.assertEqual(actual, True)

    def test_valid_date_with_invalid_values_expect_false(self):
        values = [
            "12/32/2019",
            "32/12/2019",
            "12-32-2019",
            "32-12-2019",
            "2019-13-31",
            "2019-12-32",
            "2019-1-1",
            "2019-10-1",
            "2019-1-10",
            True,
            False,
            [],
            {},
            "",
            -1,
            0,
            1,
            12122019,
            "12122019",
        ]

        for value in values:
            actual = self.validator.valid_date(value)
            self.assertEqual(actual, False)
