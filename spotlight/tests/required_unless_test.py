from spotlight.errors import REQUIRED_UNLESS_ERROR
from spotlight.tests.validator_test import ValidatorTest


class RequiredUnlessTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.value = "test"
        self.required_unless_error = REQUIRED_UNLESS_ERROR.format(
            field=self.field, other=self.other_field, value=self.value
        )

    def test_required_unless_rule_with_required_condition_expect_error(self):
        data = {"test1": "test2"}
        rules = {"test2": "required_unless:test1,test"}
        expected = self.required_unless_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_unless_rule_with_not_required_condition_expect_no_error(self):
        data = {"test1": "test"}
        rules = {"test2": "required_unless:test1,test"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_unless_rule_with_missing_field_expect_error(self):
        data = {}
        rules = {"test2": "required_unless:test1,test"}
        expected = self.required_unless_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
