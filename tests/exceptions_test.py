from typing import Any, List

import pytest

from src.spotlight.exceptions import (
    AttributeNotImplementedError,
    RuleNameAlreadyExistsError,
    InvalidDataError,
    InvalidRulesError,
    RuleNotFoundError,
)
from src.spotlight.rules import Rule
from .validator_test import ValidatorTest


class ExceptionsTest(ValidatorTest):
    def test_new_rule_without_name_expect_error(self):
        with pytest.raises(AttributeNotImplementedError):

            class NewRule(Rule):
                def passes(
                    self, field: str, value: Any, parameters: List[str], validator
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
                    self, field: str, value: Any, parameters: List[str], validator
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
                self, field: str, value: Any, parameters: List[str], validator
            ) -> bool:
                return super().passes(field, value, parameters, validator)

            @property
            def message(self) -> str:
                return super().message

        with pytest.raises(NotImplementedError):
            msg = NewRule().message

        with pytest.raises(NotImplementedError):
            NewRule().passes("", None, [], {})
