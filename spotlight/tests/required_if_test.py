from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class RequiredIfTest(ValidatorTest):
    def setUp(self):
        self.other_field = "test1"
        self.field = "test2"
        self.value = "test"
        self.required_if_error = err.REQUIRED_IF_ERROR.format(
            field=self.field,
            other=self.other_field,
            value=self.value
        )

    def test_required_if_rule_with_other_field_string_expect_error(self):
        input_values = {
            "test1": "test"
        }
        rules = {
            "test2": "required_if:test1,test"
        }
        expected = self.required_if_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_field_present_expect_no_error(self):
        input_values = {
            "test1": "test",
            "test2": "world"
        }
        rules = {
            "test2": "required_if:test1,test"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_wrong_value_no_error(self):
        input_values = {
            "test1": "test2"
        }
        rules = {
            "test2": "required_if:test1,test"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_boolean_true_expect_error(self):
        input_values = {
            "test1": True
        }
        rules = {
            "test2": "required_if:test1,true"
        }
        expected = err.REQUIRED_IF_ERROR.format(
            field=self.field,
            other=self.other_field,
            value="true"
        )

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_boolean_false_expect_error(self):
        input_values = {
            "test1": False
        }
        rules = {
            "test2": "required_if:test1,false"
        }
        expected = err.REQUIRED_IF_ERROR.format(
            field=self.field,
            other=self.other_field,
            value="false"
        )

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_if_rule_with_boolean_true_expect_no_error(self):
        input_values = {
            "test1": True,
            "test2": "I am required"
        }
        rules = {
            "test2": "required_if:test1,true"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_if_rule_with_boolean_false_expect_no_error(self):
        input_values = {
            "test1": False,
            "test2": "I am required"
        }
        rules = {
            "test2": "required_if:test1,false"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
