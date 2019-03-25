from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class UniqueTest(ValidatorTest):
    def setUp(self):
        self.field = "email"
        self.unique_error = err.UNIQUE_ERROR.format(field=self.field)

    def test_unique_rule_with_existing_email_expect_error(self):
        rules = {
            "email": "unique:user,email"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = self.unique_error

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_unique_rule_with_new_email_expect_no_error(self):
        rules = {
            "email": "unique:user,email"
        }
        input_values = {
            "email": "john.doe2@example.com"
        }
        expected = None

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_unique_rule_with_new_email_and_ignore_expect_no_error(self):
        rules = {
            "email": "unique:user,email,id,1"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = None

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_unique_rule_with_new_email_and_ignore_and_where_expect_no_error(
        self
    ):
        rules = {
            "email": "unique:user,email,id,1,site_id,1"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = None

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_unique_rule_with_existing_email_and_ignore_and_where_expect_error(
        self
    ):
        rules = {
            "email": "unique:user,email,id,2,site_id,1"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = self.unique_error

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_unique_rule_with_existing_email_and_where_expect_error(
        self
    ):
        rules = {
            "email": "unique:user,email,null,null,site_id,1"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = self.unique_error

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
