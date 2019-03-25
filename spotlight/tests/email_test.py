from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class EmailTest(ValidatorTest):
    def setUp(self):
        self.field = "email"
        self.email_error = err.INVALID_EMAIL_ERROR.format(self.field)

    def test_email_rule_with_invalid_email_expect_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": "this.is.not.a.valid.email"
        }
        expected = self.email_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_valid_email_expect_no_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_email_rule_with_boolean_false_expect_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": False
        }
        expected = self.email_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_boolean_true_expect_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": True
        }
        expected = self.email_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_integer_one_expect_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": 1
        }
        expected = self.email_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_empty_string_expect_error(self):
        rules = {
            "email": "email"
        }
        input_values = {
            "email": ""
        }
        expected = self.email_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_email_rule_with_no_input_expect_no_error(self):
        rules = {
            "email": "email"
        }
        input_values = {}
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_email_with_invalid_email_expect_false(self):
        valid_email = self.validator.valid_email("this.is.not.a.valid.email")

        self.assertEqual(valid_email, False)

    def test_valid_email_with_boolean_true_expect_false(self):
        valid_email = self.validator.valid_email(True)

        self.assertEqual(valid_email, False)

    def test_valid_email_with_boolean_false_expect_false(self):
        valid_email = self.validator.valid_email(False)

        self.assertEqual(valid_email, False)
