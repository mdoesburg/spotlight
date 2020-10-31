from typing import Any, List, Callable

from src.spotlight import Rule
from .validator_test import ValidatorTest


class EqualsOneRule(Rule):

    name = "equals_one"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        return self.valid_one(value)

    @staticmethod
    def valid_one(value):
        return value == 1

    @property
    def message(self) -> str:
        return "Value is not equal to 1."


class DynamicValidationTest(ValidatorTest):
    def test_dynamically_add_static_validation_method_expect_no_error(self):
        self.validator._dynamically_add_static_validation_methods(EqualsOneRule)

        self.assertIsNotNone(self.validator.valid_one)
        self.assertIsInstance(self.validator.valid_one, Callable)
