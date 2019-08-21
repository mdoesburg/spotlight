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
            expected = DATE_ERROR.format(field=field, value="%Y-%m-%d")
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

    def test_date_rule_and_in_rule_with_valid_values_expect_no_error(self):
        rules = {
            "date1": "date|in:2019-12-31",
            "date2": "date:%Y-%m-%d %H:%M:%S|in:2019-01-01 12:00:00",
        }
        data = {"date1": "2019-12-31", "date2": "2019-01-01 12:00:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_rule_with_format_with_valid_values_expect_no_error(self):
        rules = {"date1": "date:%Y-%m-%d", "date2": "date:%m/%d/%Y"}
        data = {"date1": "2019-12-31", "date2": "01/01/2019"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_rule_with_format_with_invalid_value_expect_error(self):
        rules = {
            "date1": "date:%Y-%m-%d",
            "date2": "date:%Y-%m-%d",
            "date3": "date:%Y-%m-%d",
        }
        data = {"date1": [], "date2": {}, "date3": 123456}

        errors = self.validator.validate(data, rules)

        for field, field_errors in errors.items():
            expected = DATE_ERROR.format(field=field, value="%Y-%m-%d")
            self.assertEqual(field_errors[0], expected)

    def test_valid_date_with_format_with_valid_values_expect_true(self):
        values = {
            "2019-12-31": "%Y-%m-%d",
            "12/31/2019": "%m/%d/%Y",
            "12312019": "%m%d%Y",
            "2019-01-01 12:00:00": "%Y-%m-%d %H:%M:%S",
            "2019": "%Y",
            "2019, 1, 1": "%Y, %m, %d",
            "Sun": "%a",
            "Thu": "%a",
            "Monday": "%A",
            "Friday": "%A",
            "0": "%w",
            "Jul": "%b",
            "Nov": "%b",
            "February": "%B",
            "August": "%B",
            "31-12-12": "%d-%m-%y",
            "14:24:15": "%H:%M:%S",
            "07:34:42": "%I:%M:%S",
            "am": "%p",
            "pm": "%p",
            "14:24:15:000001": "%H:%M:%S:%f",
            "UTC": "%Z",
            "365": "%j",
            "25": "%U",
            "11": "%W",
            "Tue Aug 16 21:30:00 1988": "%c",
            "08/16/88": "%x",
            "21:30:00": "%X",
            "%": "%%",
            "1": "%u",
            "1985-08-23T3:00:00.000": "%Y-%m-%dT%H:%M:%S.%f",
        }

        for value, date_format in values.items():
            actual = self.validator.valid_date(value, date_format)
            self.assertEqual(actual, True)

    def test_valid_date_with_format_with_invalid_values_expect_false(self):
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
            actual = self.validator.valid_date(value, date_format)
            self.assertEqual(actual, False)
