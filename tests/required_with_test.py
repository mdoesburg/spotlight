from src.spotlight.errors import REQUIRED_WITH_ERROR
from .validator_test import ValidatorTest


class RequiredWithTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.required_with_error = REQUIRED_WITH_ERROR.format(
            field=self.field, other=self.other_field
        )
        self.rules = {"test2": "required_with:test1"}

    def test_required_with_rule_with_missing_field_expect_error(self):
        data = {"test1": "hello"}
        expected = self.required_with_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_with_rule_with_field_present_expect_no_error(self):
        data = {"test1": "hello", "test2": "world"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_boolean_true_expect_no_error(self):
        data = {"test1": True, "test2": "world"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_boolean_false_expect_no_error(self):
        data = {"test1": False, "test2": "world"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_multi_requirement_and_missing_field_expect_error(
        self
    ):
        field = "test5"
        rules = {"test5": "required_with:test1,test2,test3,test4"}
        data = {"test2": "not.missing", "test4": "not.missing"}
        expected = REQUIRED_WITH_ERROR.format(
            field=field, other="test1, test2, test3, test4"
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_required_with_rule_with_all_present_expect_no_error(self):
        rules = {"test5": "required_with:test1,test2,test3,test4"}
        data = {
            "test1": "test",
            "test2": "test",
            "test3": "test",
            "test4": "test",
            "test5": "test",
        }
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get("test5")

        self.assertEqual(errs, expected)

    def test_required_with_rule_with_other_field_present_but_none_expect_error(self):
        field = "test2"
        rules = {
            "test1": "required_with:test2|string",
            "test2": "required_with:test1|string",
        }
        data = {"test1": "test", "test2": None}
        expected = REQUIRED_WITH_ERROR.format(field=field, other="test1")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_required_with_rule_with_both_none_expect_no_error(self):
        field = "test2"
        rules = {
            "test1": "required_with:test2|string",
            "test2": "required_with:test1|string",
        }
        data = {"test1": None, "test2": None}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)
