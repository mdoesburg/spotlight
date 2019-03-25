from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class ExistsTest(ValidatorTest):
    def test_exists_rule_with_existing_id_expect_no_error(self):
        field = "id"
        rules = {
            "id": "exists:user,id"
        }
        input_values = {
            "id": 1
        }
        expected = None

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)

    def test_exists_rule_with_non_existing_id_expect_error(self):
        field = "id"
        rules = {
            "id": "exists:user,id"
        }
        input_values = {
            "id": 3
        }
        expected = err.EXISTS_ERROR.format(field=field)

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_exists_rule_with_non_existing_email_for_id_expect_error(self):
        field = "email"
        other = "id"
        rules = {
            "email": "exists:user,email,id,1"
        }
        input_values = {
            "email": "john.doe2@example.com"
        }
        expected = err.EXISTS_WHERE_ERROR.format(field=field, other=other)

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_exists_rule_with_existing_email_for_id_expect_no_error(self):
        field = "email"
        rules = {
            "email": "exists:user,email,id,1"
        }
        input_values = {
            "email": "john.doe@example.com"
        }
        expected = None

        errors = self.validator_with_session.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)
