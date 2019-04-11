from spotlight.tests.validator_test import ValidatorTest


class NestedValidation(ValidatorTest):
    def test_nested_vaidation_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
            },
            "nonNested": "max:1"
        }
        input_values = {
            "nested": {
                "test": "123456"
            },
            "nonNested": "12"
        }
        expected = {
            'nested':
                 {
                     'test': ['The test field cannot be longer than 5 characters.', 'Invalid email address.']
                 },
             'nonNested': ['The nonNested field cannot be longer than 1 characters.']
        }

        self.assertEqual(expected,self.validator.validate(input_values,rules))
