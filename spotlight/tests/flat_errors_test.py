from spotlight.tests.validator_test import ValidatorTest


class FlatErrorsTest(ValidatorTest):
    def test_flat_dict_with_two_errors_expect_flat_dict(self):
        rules = {
            "email": "email|max:4",
            "password": "min:8"
        }
        input_values = {
            "email": "this.is.not.a.valid.email",
            "password": "test"
        }

        errors = self.validator.validate(input_values, rules, flat=True)

        self.assertEqual(len(errors), 3)
