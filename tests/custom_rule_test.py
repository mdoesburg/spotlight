from typing import Any, List

from src.spotlight.rules import Rule
from .validator_test import ValidatorTest


class ExactlyFiveCharsRule(Rule):
    """Exactly 5 characters"""

    name = "five_chars"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field, name="you.can.replace.this")

        return len(value) == 5

    @property
    def message(self) -> str:
        return "The {field} field has to be exactly 5 chars long {name}!"


class UppercaseRule(Rule):
    """Uppercase"""

    name = "uppercase"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return value.upper() == value

    @property
    def message(self) -> str:
        return "The {field} field must be uppercase."


class CustomRuleTest(ValidatorTest):
    def setUp(self):
        self.validator.fields = {}

    def test_custom_rule_uppercase_with_non_uppercase_string_expect_error(self):
        field = "test"
        rules = {"test": "uppercase"}
        data = {"test": "test"}
        expected = "The test field must be uppercase."

        rule = UppercaseRule()
        self.validator.register_rule(rule)
        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_custom_rule_five_chars_with_invalid_string_expect_error(self):
        field = "test"
        rules = {"test": "five_chars"}
        data = {"test": "test"}
        rule = ExactlyFiveCharsRule()
        self.validator.overwrite_fields = {
            "test": "test",
            "you.can.replace.this": "custom",
        }
        expected = rule.message.format(field=field, name="custom")

        self.validator.register_rule(rule)
        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
