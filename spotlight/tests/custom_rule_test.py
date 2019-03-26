from spotlight.tests.validator_test import ValidatorTest
from spotlight.rules import Rule


class ExactlyFiveCharsRule(Rule):
    def __init__(self):
        super().__init__()
        self.name = "five_chars"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field, name="you.can.replace.this")

        return len(value) == 5

    def message(self) -> str:
        return "The {field} field has to be exactly 5 chars long {name}!"


class UppercaseRule(Rule):
    def __init__(self):
        super().__init__()
        self.name = "uppercase"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return value.upper() == value

    def message(self) -> str:
        return "The {field} field must be uppercase."


class CustomRuleTest(ValidatorTest):
    def setUp(self):
        self.validator.fields = {}

    def test_custom_rule_uppercase_with_non_uppercase_string_expect_error(self):
        field = "test"
        rules = {
            "test": "uppercase"
        }
        input_values = {
            "test": "test"
        }
        expected = "The test field must be uppercase."

        rule = UppercaseRule()
        self.validator.register_rule(rule)
        errors = self.validator.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_custom_rule_five_chars_with_invalid_string_expect_error(self):
        field = "test"
        rules = {
            "test": "five_chars"
        }
        input_values = {
            "test": "test"
        }
        fields = {
            "test": "test",
            "you.can.replace.this": "lol"
        }
        rule = ExactlyFiveCharsRule()
        expected = rule.message().format(field=field, name="lol")

        self.validator.fields = fields
        self.validator.register_rule(rule)
        errors = self.validator.validate(input_values, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
