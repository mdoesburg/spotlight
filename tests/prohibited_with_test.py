from src.spotlight.errors import PROHIBITED_WITH_ERROR
from .validator_test import ValidatorTest


class ProhibitedWithTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.prohibited_with_error = PROHIBITED_WITH_ERROR.format(
            field=self.field, other=self.other_field
        )
        self.rules = {"test2": "prohibited_with:test1"}

    def test_prohibited_with_rule_expect_error(self):
        data = {"test1": "hello", "test2": "world"}
        expected = self.prohibited_with_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_with_rule_with_field_missing_expect_no_error(self):
        data = {"test1": "hello"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_with_rule_with_boolean_true_expect_error(self):
        data = {"test1": True, "test2": "world"}
        expected = self.prohibited_with_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_with_rule_with_boolean_false_expect_error(self):
        data = {"test1": False, "test2": "world"}
        expected = self.prohibited_with_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_with_rule_with_multi_requirement_expect_error(self):
        field = "test5"
        rules = {"test5": "prohibited_with:test1,test2,test3,test4"}
        data = {"test2": "not.missing", "test4": "not.missing", "test5": "test"}
        expected = PROHIBITED_WITH_ERROR.format(
            field=field, other="test1, test2, test3, test4"
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_with_rule_with_multi_requirement_expect_no_error(self):
        rules = {"test5": "prohibited_with:test1,test2,test3,test4"}
        data = {
            "test1": "test",
            "test2": "test",
            "test3": "test",
            "test4": "test",
        }
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get("test5")

        self.assertEqual(errs, expected)

    def test_prohibited_with_rule_with_other_field_present_but_none_expect_no_error(
        self,
    ):
        field = "test2"
        rules = {
            "test1": "prohibited_with:test2|string",
            "test2": "prohibited_with:test1|string",
        }
        data = {"test1": "test", "test2": None}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)

    def test_prohibited_with_rule_with_both_none_expect_no_error(self):
        field = "test2"
        rules = {
            "test1": "prohibited_with:test2|string",
            "test2": "prohibited_with:test1|string",
        }
        data = {"test1": None, "test2": None}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs, expected)

    def test_prohibited_with_rule_with_tuple_expect_error(self):
        field = "test"
        data = {"field,with,commas": "test", "test": "data"}
        rules = {"test": [("prohibited_with", ["field,with,commas"])]}
        expected = PROHIBITED_WITH_ERROR.format(field=field, other="field,with,commas")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_in_rule_with_list_expect_error(self):
        field = "test"
        data = {"field,with,commas": "test", "test": "data"}
        rules = {"test": [["prohibited_with", ["field,with,commas"]]]}
        expected = PROHIBITED_WITH_ERROR.format(field=field, other="field,with,commas")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
