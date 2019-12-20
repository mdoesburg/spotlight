from src.spotlight.errors import EMAIL_ERROR
from .validator_test import ValidatorTest


class CustomData:
    def __init__(self, email: str):
        self.email = email


class NestedData:
    def __init__(self, data: CustomData):
        self.data = data


class ObjectInputTest(ValidatorTest):
    def test_object_input_with_one_rule_expect_error(self):
        field = "email"
        rules = {"email": "required|email"}
        data = CustomData(email="john.doe@")
        expected = EMAIL_ERROR.format(field=field)

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_nested_object_input_with_one_rule_expect_error(self):
        field = "data.email"
        rules = {"data.email": "required|email"}
        data = CustomData(email="john.doe@")
        parent_data = NestedData(data)

        expected = {field: [EMAIL_ERROR.format(field=field)]}

        errors = self.validator.validate(parent_data, rules)

        self.assertEqual(errors, expected)
