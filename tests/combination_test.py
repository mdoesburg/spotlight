from src.spotlight.errors import EMAIL_ERROR, MIN_STRING_ERROR
from .validator_test import ValidatorTest


class CombinationTest(ValidatorTest):
    def test_combo_with_invalid_email_and_min_expect_error(self):
        field = "field1"
        rules = {"field1": "filled|email|min:5|max:255"}
        data = {"field1": "oops"}

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], EMAIL_ERROR.format(field=field))
        self.assertEqual(errs[1], MIN_STRING_ERROR.format(field=field, min=5))

    def test_before_and_after_with_custom_format_expect_no_error(self):
        rules = {
            "start_time": "date_time:%H:%M:%S|after:12:00:00|before:end_time",
            "end_time": "date_time:%H:%M:%S",
        }
        data = {"start_time": "12:30:00", "end_time": "13:00:00"}
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
