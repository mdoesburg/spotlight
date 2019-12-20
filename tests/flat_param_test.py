from .validator_test import ValidatorTest


class FlatParamTest(ValidatorTest):
    def setUp(self):
        self.rules = {
            "email": "email|max:4",
            "password": "min:8",
            "nested1.field": "min:5",
            "nested2.*": "min:5",
            "nested3.*.field": "min:5",
            "nested4.nested.field": "min:5",
        }
        self.data = {
            "email": "this.is.not.a.valid.email",
            "password": "test",
            "nested1": {"field": "test"},
            "nested2": ["test", "valid", "test"],
            "nested3": [{"field": "test"}, {"field": "valid"}, {"field": "test"}],
            "nested4": {"nested": {"field": "test"}},
        }

    def test_flat_param_true_expect_list_of_errors(self):
        errors = self.validator.validate(self.data, self.rules, flat=True)

        self.assertEqual(isinstance(errors, list), True)
        self.assertEqual(len(errors), 9)

    def test_flat_param_false_expect_dict_of_errors(self):
        errors = self.validator.validate(self.data, self.rules, flat=False)

        self.assertEqual(isinstance(errors, dict), True)
        self.assertEqual(len(errors), 8)
        self.assertEqual(len(errors.get("email")), 2)
        self.assertEqual(len(errors.get("password")), 1)
        self.assertEqual(len(errors.get("nested1.field")), 1)
        self.assertEqual(len(errors.get("nested2.0")), 1)
        self.assertEqual(len(errors.get("nested2.2")), 1)
        self.assertEqual(len(errors.get("nested3.0.field")), 1)
        self.assertEqual(len(errors.get("nested3.2.field")), 1)
        self.assertEqual(len(errors.get("nested4.nested.field")), 1)
