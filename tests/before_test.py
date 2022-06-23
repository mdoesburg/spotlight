from datetime import datetime, timedelta, date

import pytest

from src.spotlight.errors import BEFORE_ERROR
from src.spotlight.exceptions import InvalidDateTimeFormat
from .validator_test import ValidatorTest


class BeforeTest(ValidatorTest):
    def test_before_rule_with_valid_value_expect_no_error(self):
        rules = {"start_time": "date_time|before:2019-08-24 16:48:00"}
        data = {"start_time": "2019-08-24 16:28:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_value_and_invalid_time_expect_error(self):
        field = "start_time"
        rules = {"start_time": "date_time|before:2019-08-24 16:00:00"}
        data = {"start_time": "2019-08-24 16:28:00"}
        expected = BEFORE_ERROR.format(field=field, other="2019-08-24 16:00:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_without_datetime_rule_and_invalid_time_expect_error(self):
        field = "start_time"
        rules = {"start_time": "before:2019-08-24 16:00:00"}
        data = {"start_time": "2019-08-24 16:28:00"}
        expected = BEFORE_ERROR.format(field=field, other="2019-08-24 16:00:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_without_datetime_rule_and_invalid_value_expect_error(self):
        field = "start_time"
        rules = {"start_time": "before:2019-08-24 16:00:00"}
        data = {"start_time": "2019-08-24 16:28:00"}
        expected = BEFORE_ERROR.format(field=field, other="2019-08-24 16:00:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_with_invalid_values_expect_exception(self):
        values = [
            "before",
            "before:",
            "before:2019-08-24",
            "before:invalid",
            "before:2019-24-08 16:27:00",
            "before:dt2",
        ]
        data = {"dt1": "2019-08-24 16:28:00", "dt2": "invalid"}

        for value in values:
            with pytest.raises(InvalidDateTimeFormat):
                rules = {"dt1": f"date_time|{value}"}
                self.validator.validate(data, rules)

    def test_before_rule_with_custom_format_and_valid_value_expect_no_error(self):
        rules = {"start_time": "date_time:%m/%d/%Y %H:%M:%S|before:2019-08-24 16:48:00"}
        data = {"start_time": "08/24/2019 16:47:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_custom_format_and_invalid_value_expect_error(self):
        field = "start_time"
        rules = {"start_time": "date_time:%m/%d/%Y %H:%M:%S|before:2019-08-24 16:48:00"}
        data = {"start_time": "08/24/2019 16:48:00"}
        expected = BEFORE_ERROR.format(field=field, other="2019-08-24 16:48:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_with_valid_other_field_expect_no_error(self):
        rules = {"start_time": "date_time|before:end_time", "end_time": "date_time"}
        data = {"start_time": "2019-08-24 16:28:00", "end_time": "2019-08-24 16:48:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_valid_other_field_expect_error(self):
        field = "start_time"
        rules = {"start_time": "date_time|before:end_time", "end_time": "date_time"}
        data = {"start_time": "2019-08-24 16:48:00", "end_time": "2019-08-24 16:48:00"}
        expected = BEFORE_ERROR.format(field=field, other="end_time")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_with_invalid_other_field_expect_exception(self):
        rules = {"start_time": "date_time|before:end_time", "end_time": "date_time"}
        data = {"start_time": "2019-08-24 16:48:00", "end_time": "invalid"}

        with pytest.raises(InvalidDateTimeFormat):
            self.validator.validate(data, rules)

    def test_before_rule_with_format_value_expect_no_error(self):
        rules = {"start_time": "date_time:%H:%M:%S|before:12:00:00"}
        data = {"start_time": "11:59:59"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_invalid_value_expect_exception(self):
        rules = {"start_time": "date_time|before:12:00:00"}
        data = {"start_time": "2019-06-01 11:59:59"}

        with pytest.raises(InvalidDateTimeFormat):
            self.validator.validate(data, rules)

    def test_before_rule_with_python_datetime_objects_value_expect_no_error(self):
        time = datetime.utcnow()
        rules = {"start_time": "date_time|before:end_time", "end_time": "date_time"}
        data = {"start_time": time, "end_time": time + timedelta(days=1)}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_python_datetime_object_and_invalid_time_value_expect_error(
        self,
    ):
        time = datetime.utcnow()
        field = "start_time"
        rules = {"start_time": "date_time|before:end_time", "end_time": "date_time"}
        data = {"start_time": time, "end_time": time}
        expected = BEFORE_ERROR.format(field=field, other="end_time")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_before_rule_with_python_date_objects_expect_no_error(self):
        rules = {"start_date": "date_time|before:end_date", "end_date": "date_time"}
        data = {"start_date": date(2022, 2, 1), "end_date": date(2022, 2, 2)}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_python_date_objects_expect_error(self):
        rules = {"start_date": "date_time|before:end_date", "end_date": "date_time"}
        data = {"start_date": date(2022, 2, 2), "end_date": date(2022, 2, 1)}
        expected = {
            "start_date": [BEFORE_ERROR.format(field="start_date", other="end_date")]
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_python_date_and_datetime_objects_expect_no_error(self):
        rules = {
            "start_date1": "date_time|before:end_date1",
            "end_date1": "date_time",
            "start_date2": "date_time|before:end_date2",
            "end_date2": "date_time",
        }
        data = {
            "start_date1": date(2022, 2, 1),
            "end_date1": datetime.strptime(
                "2022-02-02 12:30:00",
                self.validator.config.DEFAULT_DATE_TIME_FORMAT,
            ),
            "start_date2": datetime.strptime(
                "2022-02-01 12:30:00",
                self.validator.config.DEFAULT_DATE_TIME_FORMAT,
            ),
            "end_date2": date(2022, 2, 2),
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_before_rule_with_python_date_and_datetime_objects_expect_error(self):
        rules = {
            "start_date1": "date_time|before:end_date1",
            "end_date1": "date_time",
            "start_date2": "date_time|before:end_date2",
            "end_date2": "date_time",
        }
        data = {
            "start_date1": date(2022, 2, 1),
            "end_date1": datetime.strptime(
                "2022-02-01 12:30:00",
                self.validator.config.DEFAULT_DATE_TIME_FORMAT,
            ),
            "start_date2": datetime.strptime(
                "2022-02-01 12:30:00",
                self.validator.config.DEFAULT_DATE_TIME_FORMAT,
            ),
            "end_date2": date(2022, 2, 1),
        }
        expected = {
            "start_date1": [
                BEFORE_ERROR.format(field="start_date1", other="end_date1")
            ],
            "start_date2": [
                BEFORE_ERROR.format(field="start_date2", other="end_date2")
            ],
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
