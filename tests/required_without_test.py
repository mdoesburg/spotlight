from src.spotlight.errors import REQUIRED_WITHOUT_ERROR
from .validator_test import ValidatorTest


class RequiredWithoutTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.required_without_error = REQUIRED_WITHOUT_ERROR.format(
            field=self.field, other=self.other_field
        )
        self.rules = {"test2": "required_without:test1"}

    def test_required_without_rule_with_missing_field_expect_error(self):
        data = {}
        expected = self.required_without_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_without_rule_with_field_present_expect_no_error(self):
        data = {"test2": "world"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_without_rule_with_missing_fields_expect_error(self):
        field = "test4"
        rules = {"test4": "required_without:test1,test2,test3"}
        data = {"test2": "not.missing"}
        expected = REQUIRED_WITHOUT_ERROR.format(
            field=field, other="test1, test2, test3"
        )

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)

    def test_required_without_rule_with_both_fields_present_but_none_expect_error(self):
        field = "test2"
        rules = {
            "test1": "required_without:test2|string",
            "test2": "required_without:test1|string",
        }
        data = {"test1": None, "test2": None}
        expected = REQUIRED_WITHOUT_ERROR.format(field=field, other="test1")

        errors = self.validator.validate(data, rules)
        errs = errors.get(field)

        self.assertEqual(errs[0], expected)
