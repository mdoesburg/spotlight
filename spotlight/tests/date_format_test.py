from spotlight.errors import DATE_FORMAT_ERROR
from spotlight.tests.validator_test import ValidatorTest


class DateFormatTest(ValidatorTest):
    def test_date_format_rule_with_valid_values_expect_no_error(self):
        rules = {"date1": "date_format:%Y-%m-%d", "date2": "date_format:%m/%d/%Y"}
        data = {"date1": "2019-12-31", "date2": "01/01/2019"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_format_rule_with_invalid_value_expect_error(self):
        rules = {
            "date1": "date_format:%Y-%m-%d",
            "date2": "date_format:%Y-%m-%d",
            "date3": "date_format:%Y-%m-%d",
        }
        data = {"date1": [], "date2": {}, "date3": 123456}

        errors = self.validator.validate(data, rules)

        for field, field_errors in errors.items():
            expected = DATE_FORMAT_ERROR.format(field=field, value="%Y-%m-%d")
            self.assertEqual(field_errors[0], expected)

    def test_valid_date_format_with_valid_values_expect_true(self):
        values = {
            "2019-12-31": "%Y-%m-%d",
            "12/31/2019": "%m/%d/%Y",
            "12312019": "%m%d%Y",
            "2019": "%Y",
            "2019, 1, 1": "%Y, %m, %d",
        }

        for value, date_format in values.items():
            actual = self.validator.valid_date_format(value, date_format)
            self.assertEqual(actual, True)

    def test_valid_date_format_with_invalid_values_expect_false(self):
        values = [
            "12/32/2019",
            "32/12/2019",
            "12-32-2019",
            "32-12-2019",
            "2019-13-31",
            "2019-12-32",
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
        date_formats = [
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
            "%Y-%m-%d",
        ]

        for value, date_format in zip(values, date_formats):
            actual = self.validator.valid_date_format(value, date_format)
            self.assertEqual(actual, False)
