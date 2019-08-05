import pytest

from spotlight.exceptions import RuleNotFoundError
from spotlight.tests.validator_test import ValidatorTest


class InvalidRuleTest(ValidatorTest):
    def test_empty_rule_expect_no_error(self):
        rules = {"test": ""}
        input_values = {"test": "John Doe"}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(len(errors), 0)

    def test_non_existent_rule_expect_rule_not_found_error(self):
        rules = {"test": "lol"}
        input_values = {"test": "John Doe"}

        with pytest.raises(RuleNotFoundError):
            self.validator.validate(input_values, rules)
