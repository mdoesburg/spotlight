from src.spotlight.errors import PROHIBITED_UNLESS_ERROR
from .validator_test import ValidatorTest


class ProhibitedUnlessTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.value = "test"
        self.prohibited_unless_error = PROHIBITED_UNLESS_ERROR.format(
            field=self.field, other=self.other_field, value=self.value
        )

    def test_prohibited_unless_rule_with_required_condition_expect_error(self):
        data = {"test1": "test2", "test2": "world"}
        rules = {"test2": "prohibited_unless:test1,test"}
        expected = self.prohibited_unless_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_unless_rule_with_not_required_condition_expect_no_error(self):
        data = {"test1": "test", "test2": "world"}
        rules = {"test2": "prohibited_unless:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_nested_prohibited_unless_rule_with_required_condition_expect_error(self):
        data = {"test1": {"test1": "test2"}, "test2": "world"}
        rules = {"test2": "prohibited_unless:test1.test1,test"}
        expected = PROHIBITED_UNLESS_ERROR.format(
            field=self.field, other="test1.test1", value=self.value
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_nested_prohibited_unless_rule_with_not_required_condition_expect_no_error(
        self,
    ):
        data = {"test1": {"test1": "test"}, "test2": "world"}
        rules = {"test2": "prohibited_unless:test1.test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_unless_rule_with_missing_field_expect_error(self):
        data = {"test2": "world"}
        rules = {"test2": "prohibited_unless:test1,test"}
        expected = self.prohibited_unless_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_unless_rule_with_field_present_but_none_expect_no_error(self):
        field = "test2"
        data = {"test1": "not_some_value", "test2": None}
        rules = {"test1": "string", "test2": "prohibited_unless:test1,some_value"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)
