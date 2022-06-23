from src.spotlight.errors import AFTER_ERROR, BEFORE_ERROR
from .validator_test import ValidatorTest


class ListNotationTest(ValidatorTest):
    def test_list_notation_with_date_time_rule_expect_no_error(self):
        rules = {
            "field1": ["required", "date_time"],
            "field2": ["required", "date_time"],
        }
        data = {
            "field1": "2019-12-31 23:59:59",
            "field2": "2019-01-01 00:00:00",
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_notation_with_in_rule_expect_no_error(self):
        rules = {"field1": ["in:value1,value2,value3"]}
        data = {"field1": "value2"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_notation_with_date_time_and_after_rule_expect_error(self):
        rules = {"field1": ["date_time", "after:2020-01-01 00:00:00"]}
        data = {"field1": "2019-12-31 23:59:59"}
        expected = {
            "field1": [AFTER_ERROR.format(field="field1", other="2020-01-01 00:00:00")]
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)

    def test_list_notation_with_date_time_and_before_rule_expect_error(self):
        rules = {"field1": ["date_time", "before:2020-01-01 00:00:00"]}
        data = {"field1": "2020-01-01 00:00:01"}
        expected = {
            "field1": [BEFORE_ERROR.format(field="field1", other="2020-01-01 00:00:00")]
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
