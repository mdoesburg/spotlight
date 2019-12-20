from src.spotlight.errors import URL_ERROR
from .validator_test import ValidatorTest


class UrlTest(ValidatorTest):
    def test_url_rule_with_invalid_urls_expect_errors(self):
        rules = {"url1": "url", "url2": "url", "url3": "url"}
        data = {
            "url1": "this.is.not.a.valid.url",
            "url2": "http",
            "url3": "www.google.com",
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 3)
        for field, errs in errors.items():
            expected = URL_ERROR.format(field=field)
            self.assertEqual(errs[0], expected)

    def test_url_rule_with_valid_urls_expect_no_errors(self):
        rules = {
            "url1": "url",
            "url2": "url",
            "url3": "url",
            "url4": "url",
            "url5": "url",
            "url6": "url",
            "url7": "url",
        }
        data = {
            "url1": "http://google.com",
            "url2": "https://google.com",
            "url3": "http://www.google.com",
            "url4": "http://localhost",
            "url5": "http://localhost:8080",
            "url6": "http://localhost:8080/test/",
            "url7": "http://test.dev/test/",
        }
        expected = None

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 0)
        for field, errs in errors.items():
            self.assertEqual(errs, expected)

    def test_valid_url_with_boolean_true_expect_false(self):
        valid_url = self.validator.valid_url(True)

        self.assertEqual(valid_url, False)

    def test_valid_url_with_valid_url_expect_true(self):
        valid_url = self.validator.valid_url("https://google.com")

        self.assertEqual(valid_url, True)
