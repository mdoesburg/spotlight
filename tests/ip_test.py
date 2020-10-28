from src.spotlight.errors import IP_ERROR
from .validator_test import ValidatorTest


class IpTest(ValidatorTest):
    def test_ip_rule_with_invalid_ips_expect_errors(self):
        rules = {"ip1": "ip", "ip2": "ip", "ip3": "ip"}
        data = {
            "ip1": "this.is.not.valid",
            "ip2": "255.255.255.256",
            "ip3": "www.google.com",
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 3)
        for field, errs in errors.items():
            expected = IP_ERROR.format(field=field)
            self.assertEqual(errs[0], expected)

    def test_ip_rule_with_valid_ips_expect_no_errors(self):
        rules = {"ip1": "ip", "ip2": "ip", "ip3": "ip", "ip4": "ip", "ip5": "ip"}
        data = {
            "ip1": "192.168.1.1",
            "ip2": "0.0.0.0",
            "ip3": "255.255.255.255",
            "ip4": 3232235777,
            "ip5": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        }
        expected = None

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 0)
        for field, errs in errors.items():
            self.assertEqual(errs, expected)

    def test_valid_ip_with_boolean_true_expect_true(self):
        valid_ip = self.validator.valid_ip(True)

        self.assertEqual(valid_ip, True)

    def test_valid_ip_with_integer_expect_true(self):
        # String value:  192.168.1.1
        # Binary:        11000000 . 10101000 . 00000001 . 00000001
        # Integer:       3232235777
        valid_ip = self.validator.valid_ip(3232235777)

        self.assertEqual(valid_ip, True)

    def test_valid_ip_with_list_expect_false(self):
        valid_ip = self.validator.valid_ip([])

        self.assertEqual(valid_ip, False)
