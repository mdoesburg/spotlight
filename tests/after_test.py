from datetime import datetime, timedelta

import pytest

from src.spotlight.errors import AFTER_ERROR
from src.spotlight.exceptions import InvalidDateTimeFormat
from .validator_test import ValidatorTest


class AfterTest(ValidatorTest):
    def test_after_rule_with_valid_value_expect_no_error(self):
        rules = {"end_time": "date_time|after:2019-08-24 16:28:00"}
        data = {"end_time": "2019-08-24 16:48:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_rule_with_value_and_invalid_time_expect_error(self):
        field = "end_time"
        rules = {"end_time": "date_time|after:2019-08-24 17:00:00"}
        data = {"end_time": "2019-08-24 16:28:00"}
        expected = AFTER_ERROR.format(field=field, other="2019-08-24 17:00:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_after_rule_with_invalid_values_expect_exception(self):
        values = [
            "after",
            "after:",
            "after:2019-08-24",
            "after:invalid",
            "after:2019-24-08 16:27:00",
            "after:dt2",
        ]
        data = {"dt1": "2019-08-24 16:28:00", "dt2": "invalid"}

        for value in values:
            with pytest.raises(InvalidDateTimeFormat):
                rules = {"dt1": f"date_time|{value}"}
                self.validator.validate(data, rules)

    def test_after_rule_with_custom_format_and_valid_value_expect_no_error(self):
        rules = {"end_time": "date_time:%m/%d/%Y %H:%M:%S|after:2019-08-24 16:46:00"}
        data = {"end_time": "08/24/2019 16:47:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_rule_with_custom_format_and_invalid_value_expect_error(self):
        field = "end_time"
        rules = {"end_time": "date_time:%m/%d/%Y %H:%M:%S|after:2019-08-24 16:48:00"}
        data = {"end_time": "08/24/2019 16:48:00"}
        expected = AFTER_ERROR.format(field=field, other="2019-08-24 16:48:00")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_after_rule_with_valid_other_field_expect_no_error(self):
        rules = {"start_time": "date_time", "end_time": "date_time|after:start_time"}
        data = {"start_time": "2019-08-24 16:28:00", "end_time": "2019-08-24 16:48:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_rule_with_valid_other_field_expect_error(self):
        field = "end_time"
        rules = {"start_time": "date_time", "end_time": "date_time|after:start_time"}
        data = {"start_time": "2019-08-24 16:48:00", "end_time": "2019-08-24 16:48:00"}
        expected = AFTER_ERROR.format(field=field, other="start_time")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_after_rule_with_invalid_other_field_expect_exception(self):
        rules = {"start_time": "date_time", "end_time": "date_time|after:start_time"}
        data = {"start_time": "invalid", "end_time": "2019-08-24 16:48:00"}

        with pytest.raises(InvalidDateTimeFormat):
            self.validator.validate(data, rules)

    def test_after_rule_with_format_value_expect_no_error(self):
        rules = {"start_time": "date_time:%H:%M:%S|after:12:00:00"}
        data = {"start_time": "12:00:01"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_rule_with_invalid_value_expect_exception(self):
        rules = {"start_time": "date_time|after:12:00:00"}
        data = {"start_time": "2019-06-01 12:00:01"}

        with pytest.raises(InvalidDateTimeFormat):
            self.validator.validate(data, rules)

    def test_after_rule_with_python_datetime_objects_value_expect_no_error(self):
        time = datetime.utcnow()
        rules = {"start_time": "date_time", "end_time": "date_time|after:start_time"}
        data = {"start_time": time, "end_time": time + timedelta(days=1)}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_after_rule_with_python_datetime_object_and_invalid_time_value_expect_error(self):
        time = datetime.utcnow()
        field = "end_time"
        rules = {"start_time": "date_time", "end_time": "date_time|after:start_time"}
        data = {"start_time": time, "end_time": time}
        expected = AFTER_ERROR.format(field=field, other="start_time")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
