from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class Input:
    def __init__(self, email: str):
        self.email = email


class Nested:
    def __init__(self, input: Input):
        self.input = input


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

        self.assertEqual(expected,errs[0])

    def test_nested_object_input_with_one_rule_expect_error(self):
        rules = {
            "input.email": "required|email"
        }
        command = Input(
            email="john.doe@"
        )
        parent_command = Nested(command)

        expected = {'input.email': ['Invalid email address.']}

        errors = self.validator.validate(parent_command, rules)

        self.assertEqual(expected, errors)
