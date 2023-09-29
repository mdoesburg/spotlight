from src.spotlight.errors import PROHIBITED_IF_ERROR
from .validator_test import ValidatorTest


class ProhibitedIfTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.value = "test"
        self.prohibited_if_error = PROHIBITED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=self.value
        )

    def test_prohibited_if_rule_with_other_field_string_expect_error(self):
        data = {"test1": "test", "test2": "world"}
        rules = {"test2": "prohibited_if:test1,test"}
        expected = self.prohibited_if_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_if_rule_with_field_missing_expect_no_error(self):
        data = {"test1": "test"}
        rules = {"test2": "prohibited_if:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_wrong_value_expect_no_error(self):
        data = {"test1": "test2", "test2": "world"}
        rules = {"test2": "prohibited_if:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_boolean_true_expect_error(self):
        data = {"test1": True, "test2": "world"}
        rules = {"test2": "prohibited_if:test1,True"}
        expected = PROHIBITED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=True
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_if_rule_with_boolean_false_expect_error(self):
        data = {"test1": False, "test2": "world"}
        rules = {"test2": "prohibited_if:test1,False"}
        expected = PROHIBITED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=False
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_if_rule_with_boolean_true_expect_no_error(self):
        data = {"test1": True, "test2": "I am not prohibited"}
        rules = {"test2": "prohibited_if:test1,true"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_boolean_false_expect_no_error(self):
        data = {"test1": False, "test2": "I not prohibited"}
        rules = {"test2": "prohibited_if:test1,false"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_integer_expect_no_error(self):
        data = {"test1": 1, "test2": "I am not prohibited"}
        rules = {"test2": "prohibited_if:test1,2"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_integer_expect_error(self):
        data = {"test1": 1, "test2": "I am prohibited"}
        rules = {"test2": "prohibited_if:test1,1"}
        expected = PROHIBITED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=1
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_if_rule_with_nested_integer_expect_no_error(self):
        data = {"test1": {"test1": 1}, "test2": "I am not prohibited"}
        rules = {"test2": "prohibited_if:test1.test1,2"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_if_rule_with_nested_integer_expect_error(self):
        data = {"test1": {"test1": 1}, "test2": "I am prohibited"}
        rules = {"test2": "prohibited_if:test1.test1,1"}
        expected = PROHIBITED_IF_ERROR.format(
            field=self.field, other="test1.test1", value=1
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_if_rule_with_field_present_but_none_expect_no_error(self):
        field = "test2"
        data = {"test1": "some_value", "test2": None}
        rules = {"test1": "string", "test2": "prohibited_if:test1,some_value"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)
