from spotlight.tests.validator_test import ValidatorTest


class NestedValidation(ValidatorTest):
    def test_nested_vaidation_expect_error(self):
        rules = {
            "nested" : {
                "test" : "max:5"
            },
            "nonNested" : "max:1"
        }
        input_values = {
            "nested" : {
                "test" : "123456"
            },
            "nonNested" : "12"
        }

        print(self.validator.validate(input_values,rules))
