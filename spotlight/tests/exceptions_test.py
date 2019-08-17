from typing import Any

import pytest

from spotlight.exceptions import (
    AttributeNotImplementedError,
    RuleNameAlreadyExistsError,
    InvalidDataError,
    InvalidRulesError,
    RuleNotFoundError,
)
from spotlight.rules import Rule
from spotlight.tests.validator_test import ValidatorTest


class ExceptionsTest(ValidatorTest):
    def test_new_rule_without_name_expect_error(self):
        with pytest.raises(AttributeNotImplementedError):

            class NewRule(Rule):
                def passes(
                    self, field: str, value: Any, rule_values: str, data: dict
                ) -> bool:
                    return True

                @property
                def message(self) -> str:
                    return "Hello World!"

            self.validator.register_rule(NewRule())

    def test_new_rule_with_existing_name_expect_error(self):
        with pytest.raises(RuleNameAlreadyExistsError):

            class NewRule(Rule):
                name = "required"

                def passes(
                    self, field: str, value: Any, rule_values: str, data: dict
                ) -> bool:
                    return True

                @property
                def message(self) -> str:
                    return "Hello World!"

            self.validator.register_rule(NewRule())

    def test_validate_with_invalid_data_type_expect_error(self):
        with pytest.raises(InvalidDataError):
            self.validator.validate(data=[], rules={})

    def test_validate_with_invalid_rules_type_expect_error(self):
        with pytest.raises(InvalidRulesError):
            self.validator.validate(data={}, rules=[])

    def test_empty_rule_expect_error(self):
        rules = {"test": ""}
        data = {"test": "John Doe"}

        with pytest.raises(RuleNotFoundError):
            self.validator.validate(data, rules)

    def test_non_existent_rule_expect_rule_not_found_error(self):
        rules = {"test": "not_a_rule"}
        data = {"test": "John Doe"}

        with pytest.raises(RuleNotFoundError):
            self.validator.validate(data, rules)

    def test_rule_abstract_methods_with_super_call_expect_not_implemented_error(self):
        class NewRule(Rule):
            name = "new_rule"

            def passes(
                    self, field: str, value: Any, rule_values: str, data: dict
            ) -> bool:
                return super().passes(field, value, rule_values, data)

            @property
            def message(self) -> str:
                return super().message

        with pytest.raises(NotImplementedError):
            print(NewRule().message)

        with pytest.raises(NotImplementedError):
            NewRule().passes("", None, "", {})

