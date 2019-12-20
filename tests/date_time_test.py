from datetime import datetime

from src.spotlight import config
from src.spotlight.errors import DATE_TIME_ERROR
from .validator_test import ValidatorTest


class DateTimeTest(ValidatorTest):
    def test_date_time_rule_with_valid_values_expect_no_error(self):
        rules = {"date_time1": "date_time", "date_time2": "date_time"}
        data = {
            "date_time1": "2019-12-31 23:59:59",
            "date_time2": "2019-01-01 00:00:00",
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_time_rule_with_invalid_value_expect_error(self):
        rules = {"date_time1": "date_time", "date_time2": "date_time"}
        data = {"date_time1": "", "date_time2": 102323}

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors) > 0, True)
        for field, field_errors in errors.items():
            expected = DATE_TIME_ERROR.format(field=field, format="%Y-%m-%d %H:%M:%S")
            self.assertEqual(field_errors[0], expected)

    def test_valid_date_time_with_valid_values_expect_true(self):
        values = ["2019-12-31 23:59:59", "2019-01-01 00:00:00", "2019-01-01 23:59:59"]

        for value in values:
            actual = self.validator.valid_date_time(value)
            self.assertEqual(actual, True)

    def test_valid_date_time_with_invalid_values_expect_false(self):
        values = [
            "2019-12-01 24:00:00",
            "2019-12-01 00:60:00",
            "2019-12-01 00:00:60",
            "12/32/2019 00:00:00",
            "32/12/2019 00:00:00",
            "12-32-2019 00:00:00",
            "32-12-2019 00:00:00",
            "2019-13-31 00:00:00",
            "2019-12-32 00:00:00",
            "2019-1-1 00:00:00",
            "2019-10-1 00:00:00",
            "2019-1-10 00:00:00",
            "2019-01-01 0:00:00",
            "2019-01-01 00:0:00",
            "2019-01-01 00:00:0",
            True,
            False,
            [],
            {},
            "",
            -1,
            0,
            1,
            12122019,
            "12122019 000000",
        ]

        for value in values:
            actual = self.validator.valid_date_time(value)
            self.assertEqual(actual, False)

    def test_date_time_rule_and_in_rule_with_valid_values_expect_no_error(self):
        rules = {
            "date_time1": "date_time:%Y-%m-%d|in:2019-12-31",
            "date_time2": "date_time|in:2019-01-01 12:00:00",
        }
        data = {"date_time1": "2019-12-31", "date_time2": "2019-01-01 12:00:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_time_rule_with_format_with_valid_values_expect_no_error(self):
        rules = {"date_time1": "date_time:%Y-%m-%d", "date_time2": "date_time:%m/%d/%Y"}
        data = {"date_time1": "2019-12-31", "date_time2": "01/01/2019"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_date_time_rule_with_format_with_invalid_value_expect_error(self):
        rules = {
            "date_time1": "date_time:%Y-%m-%d",
            "date_time2": "date_time:%Y-%m-%d",
            "date_time3": "date_time:%Y-%m-%d",
        }
        data = {"date_time1": [], "date_time2": {}, "date_time3": 123456}

        errors = self.validator.validate(data, rules)

        for field, field_errors in errors.items():
            expected = DATE_TIME_ERROR.format(field=field, format="%Y-%m-%d")
            self.assertEqual(field_errors[0], expected)

    def test_valid_date_time_with_format_with_valid_values_expect_true(self):
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
            "2019-05-17T19:59:19+0000": "%Y-%m-%dT%H:%M:%S%z",
        }

        for value, date_format in values.items():
            actual = self.validator.valid_date_time(value, date_format)
            self.assertEqual(actual, True)

    def test_date_time_rule_with_date_time_objects_expect_no_errors(self):
        dt1 = datetime.strptime("2019-05-16T20:59:19+0000", "%Y-%m-%dT%H:%M:%S%z")
        dt2 = datetime.strptime("2019-05-17 19:59:19", config.DEFAULT_DATE_TIME_FORMAT)
        dt3 = datetime.strptime("22/09/2020 18:59:19+0400", "%d/%m/%Y %H:%M:%S%z")

        rules = {
            "date_time1": "date_time",
            "date_time2": "date_time",
            "date_time3": "date_time",
        }
        data = {"date_time1": dt1, "date_time2": dt2, "date_time3": dt3}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_valid_date_time_with_format_with_date_time_object_expect_true(self):
        dt = datetime.strptime("2019-05-17 19:59:19", config.DEFAULT_DATE_TIME_FORMAT)

        actual = self.validator.valid_date_time(dt)
        self.assertEqual(actual, True)

    def test_valid_date_time_with_format_with_invalid_values_expect_false(self):
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
        date_time_formats = [
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

        for value, date_time_format in zip(values, date_time_formats):
            actual = self.validator.valid_date_time(value, date_time_format)
            self.assertEqual(actual, False)
