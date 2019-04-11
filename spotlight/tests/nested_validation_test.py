from spotlight.tests.validator_test import ValidatorTest
from spotlight.validator import Validator


class NestedValidation(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}
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

    def test_double_nested_validation_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "doubleNested": {
                    "test2": "max:2"
                },
            },
            "nonNested": "max:1"
        }
        input_values = {
            "nested": {
                "test": "123456",
                "doubleNested": {
                    "test2": "12222"
                },
            },
            "nonNested": "12"
        }
        expected = {
            'nested':
                 {
                     'test': ['The test field cannot be longer than 5 characters.', 'Invalid email address.'],
                     "doubleNested": {
                         "test2": ['The test2 field cannot be longer than 2 characters.']
                     }
                 },
             'nonNested': ['The nonNested field cannot be longer than 1 characters.']
        }
        self.assertEqual(expected,self.validator.validate(input_values,rules))

    def test_double_nested_validation_custom_message_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "doubleNested": {
                    "test2": "max:2"
                },
            },
            "nonNested": "max:1"
        }
        input_values = {
            "nested": {
                "test": "123456",
                "doubleNested": {
                    "test2": "12222"
                },
            },
            "nonNested": "12"
        }
        new_message = "Hey! The {field} field has to be at least {max} chars!"
        messages = {
            "test2.max": new_message
        }
        expected = {
            'nested':
                 {
                     'test': ['The test field cannot be longer than 5 characters.', 'Invalid email address.'],
                     "doubleNested": {
                         "test2": ['Hey! The test2 field has to be at least 2 chars!']
                     }
                 },
             'nonNested': ['The nonNested field cannot be longer than 1 characters.']
        }

        self.validator.overwrite_messages= messages

        self.assertEqual(expected,self.validator.validate(input_values,rules))

    def test_double_nested_validation_custom_field_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "doubleNested": {
                    "test2": "max:2"
                },
            },
            "nonNested": "max:1"
        }
        input_values = {
            "nested": {
                "test": "123456",
                "doubleNested": {
                    "test2": "12222"
                },
            },
            "nonNested": "12"
        }
        fields = {
            "test2": "custom"
        }
        expected = {
            'nested':
                {
                    'test': ['The test field cannot be longer than 5 characters.', 'Invalid email address.'],
                    "doubleNested": {
                         "test2": ['The custom field cannot be longer than 2 characters.']
                    }
                },
            'nonNested': ['The nonNested field cannot be longer than 1 characters.']
        }

        self.validator.overwrite_fields = fields

        self.assertEqual(expected, self.validator.validate(input_values, rules))

    def test_double_nested_validation_with_new_values_expect_error(self):
        rules = {
            "nested": {
                "test": "max:5|email",
                "doubleNested": {
                    "test2": "in:val1,val2,val3"
                },
            },
            "nonNested": "max:1"
        }
        input_values = {
            "nested": {
                "test": "123456",
                "doubleNested": {
                    "test2": "12222"
                },
            },
            "nonNested": "12"
        }
        new_values = "piet, henk, jan"
        values = {
            "test2": {
                "values": new_values
            }
        }
        expected = {
            'nested':
                {
                    'test': ['The test field cannot be longer than 5 characters.', 'Invalid email address.'],
                    "doubleNested": {
                       'test2': ['The test2 field must be one of the following values: piet, henk, jan.']
                    },
                },
            'nonNested': ['The nonNested field cannot be longer than 1 characters.']
        }

        self.validator.overwrite_values= values
        self.assertEqual(expected, self.validator.validate(input_values, rules))

