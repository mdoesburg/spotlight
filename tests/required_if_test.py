from src.spotlight.errors import REQUIRED_IF_ERROR
from .validator_test import ValidatorTest


class RequiredIfTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.value = "test"
        self.required_if_error = REQUIRED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=self.value
        )

    def test_required_if_rule_with_other_field_string_expect_error(self):
        data = {"test1": "test"}
        rules = {"test2": "required_if:test1,test"}
        expected = self.required_if_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_field_present_expect_no_error(self):
        data = {"test1": "test", "test2": "world"}
        rules = {"test2": "required_if:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_wrong_value_no_error(self):
        data = {"test1": "test2"}
        rules = {"test2": "required_if:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_boolean_true_expect_error(self):
        data = {"test1": True}
        rules = {"test2": "required_if:test1,True"}
        expected = REQUIRED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=True
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_boolean_false_expect_error(self):
        data = {"test1": False}
        rules = {"test2": "required_if:test1,False"}
        expected = REQUIRED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=False
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_boolean_true_expect_no_error(self):
        data = {"test1": True, "test2": "I am required"}
        rules = {"test2": "required_if:test1,true"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_boolean_false_expect_no_error(self):
        data = {"test1": False, "test2": "I am required"}
        rules = {"test2": "required_if:test1,false"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_integer_expect_no_error(self):
        data = {"test1": 1, "test2": "I am required"}
        rules = {"test2": "required_if:test1,1"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_integer_expect_error(self):
        data = {"test1": 1}
        rules = {"test2": "required_if:test1,1"}
        expected = REQUIRED_IF_ERROR.format(
            field=self.field, other=self.other_field, value=1
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_nested_integer_expect_no_error(self):
        data = {"test1": {"test1": 1}, "test2": "I am required"}
        rules = {"test2": "required_if:test1.test1,1"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_nested_integer_expect_error(self):
        data = {"test1": {"test1": 1}}
        rules = {"test2": "required_if:test1.test1,1"}
        expected = REQUIRED_IF_ERROR.format(
            field=self.field, other="test1.test1", value=1
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_field_present_but_none_expect_error(self):
        field = "test2"
        rules = {"test1": "string", "test2": "required_if:test1,some_value"}
        data = {"test1": "some_value", "test2": None}
        expected = REQUIRED_IF_ERROR.format(
            field=field, other="test1", value="some_value"
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
