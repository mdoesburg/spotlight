from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class CombinationTest(ValidatorTest):
    def test_combo_with_invalid_email_and_min_expect_error(self):
        field = "field1"
        rules = {
            "field1": "filled|email|min:5|max:255"
        }
        input_values = {
            "field1": "oops"
        }

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], err.INVALID_EMAIL_ERROR.format(field=field))
        self.assertEqual(errs[1], err.MIN_STRING_ERROR.format(field=field, min=5))
