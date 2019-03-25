from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class Input:
    def __init__(self, email: str):
        self.email = email

    def test(self):
        return self.email


class ObjectInputTest(ValidatorTest):
    def test_object_input_with_one_rule_expect_error(self):
        field = "email"
        rules = {
            "email": "required|email"
        }
        command = Input(
            email="john.doe@"
        )
        expected = err.INVALID_EMAIL_ERROR

        errors = self.validator.validate(command, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
