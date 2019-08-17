from spotlight.errors import EMAIL_ERROR, MIN_STRING_ERROR
from spotlight.tests.validator_test import ValidatorTest


class CombinationTest(ValidatorTest):
    def test_combo_with_invalid_email_and_min_expect_error(self):
        field = "field1"
        rules = {"field1": "filled|email|min:5|max:255"}
        data = {"field1": "oops"}

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], EMAIL_ERROR.format(field=field))
        self.assertEqual(errs[1], MIN_STRING_ERROR.format(field=field, min=5))
