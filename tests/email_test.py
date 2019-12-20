from src.spotlight.errors import EMAIL_ERROR
from .validator_test import ValidatorTest


class EmailTest(ValidatorTest):
    def setUp(self):
        self.field = "email"
        self.email_error = EMAIL_ERROR.format(field=self.field)

    def test_email_rule_with_invalid_email_expect_error(self):
        rules = {"email": "email"}
        data = {"email": "this.is.not.a.valid.email"}
        expected = self.email_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_valid_email_expect_no_error(self):
        rules = {"email": "email"}
        data = {"email": "john.doe@example.com"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_email_rule_with_empty_string_expect_error(self):
        rules = {"email": "email"}
        data = {"email": ""}
        expected = self.email_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_no_input_expect_no_error(self):
        rules = {"email": "email"}
        data = {}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_email_with_invalid_values_expect_false(self):
        invalid_emails = [1, True, False, "test", "test@", "@"]

        for invalid_email in invalid_emails:
            actual = self.validator.valid_email(invalid_email)
            self.assertEqual(actual, False)

    def test_valid_email_with_valid_values_expect_true(self):
        valid_emails = ["a@a", "test@example", "test@example.com"]

        for valid_email in valid_emails:
            actual = self.validator.valid_email(valid_email)
            self.assertEqual(actual, True)
