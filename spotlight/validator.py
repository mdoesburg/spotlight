from typing import Union, List

from sqlalchemy.orm import Session

from spotlight import errors as err
from spotlight import rules as rls


class Validator:
    def __init__(self, session: Session = None):
        self._session = session
        self._session_required_rules = ["unique", "exists"]
        self._implicit_rules = []

        self._rules = None
        self._input = None
        self._errors = {}
        self._stop = False

        self.messages = {}
        self.fields = {}
        self.values = {}

        self.custom_rules: List[rls.BaseRule] = [
            rls.RequiredRule(),
            rls.RequiredWithoutRule(),
            rls.RequiredWithRule(),
            rls.RequiredIfRule(),
            rls.NotWithRule(),
            rls.FilledRule(),
            rls.EmailRule(),
            rls.UrlRule(),
            rls.IpRule(),
            rls.MinRule(),
            rls.MaxRule(),
            rls.InRule(),
            rls.AlphaNumRule(),
            rls.AlphaNumSpaceRule(),
            rls.StringRule(),
            rls.IntegerRule(),
            rls.BooleanRule(),
            rls.Uuid4Rule(),
            rls.UniqueRule(self._session),
            rls.ExistsRule(self._session)
        ]

        self._setup_custom_rules()

    def _setup_custom_rules(self):
        for r in self.custom_rules:
            if r.implicit:
                self._implicit_rules.append(r.name)

    def _custom_rules(self):
        custom_rules = {}
        for r in self.custom_rules:
            custom_rules[r.name] = r

        return custom_rules

    def register_custom_rule(self, rule: rls.BaseRule):
        self.custom_rules.append(rule)
        if rule.implicit:
            self._implicit_rules.append(rule.name)

    def validate(
            self,
            input_values: Union[dict, object],
            rules: dict,
            flat: bool = False
    ) -> Union[dict, list]:
        """Validate input with given rules"""
        self._rules = rules
        self._input = input_values
        self._errors = {}
        self._stop = False

        # Transform input to dictionary
        if not isinstance(self._input, dict):
            self._input = self._input.__dict__

        # Iterate over fields
        for field in self._rules:
            rules = self._rules.get(field).split("|")
            # Iterate over rules
            for rule in rules:
                # Verify that rule isn't empty
                if rule != "":
                    # Split rule name and values
                    rule_name, *values = rule.split(":")
                    print(rule_name)
                    # Check if session needs for rule
                    self._session_check(rule_name)

                    # Check if field is validatable
                    if self._is_validatable(rule_name, field):
                        # Check if rule exists
                        if rule_name in self._custom_rules():
                            r = self._custom_rules().get(rule_name)

                            # Execute correct validation method
                            value = self._input.get(field)
                            if isinstance(r, rls.Rule):
                                passed = r.passes(field, value)
                            elif isinstance(r, rls.InputDependentRule):
                                passed = r.passes(field, value, self._input)
                            elif isinstance(r, rls.DependentRule):
                                passed = r.passes(field, values, self._input)

                            if not passed:
                                self._add_error(
                                    rule_name,
                                    field,
                                    r.message(),
                                    r.message_fields
                                )

                                if r.stop:
                                    break
                        else:
                            raise Exception(
                                err.RULE_NOT_FOUND.format(rule=rule_name)
                            )

                    # Stop validation
                    if self._stop:
                        break

        self._overwrite_errors()

        if flat:
            return self._flatten_errors()

        return self._errors

    def _flatten_errors(self) -> list:
        new_errors = []
        for key, val in self._errors.items():
            for error in self._errors.get(key):
                new_errors.append(error)

        return new_errors

    def _is_validatable(self, rule, field):
        return self._present_or_rule_is_implicit(rule, field)

    def _present_or_rule_is_implicit(self, rule, field):
        return self._validate_present(field) or self._is_implicit(rule)

    def _validate_present(self, field):
        return field in self._input

    def _is_implicit(self, rule):
        return rule in self._implicit_rules

    def _session_check(self, rule_name):
        if self._rule_requires_session(rule_name):
            raise Exception(
                err.NO_SESSION_ERROR.format(rule=rule_name)
            )

    def _rule_requires_session(self, rule_name):
        return (
            rule_name in self._session_required_rules and self._session is None
        )

    def _overwrite_error(self, field, rule):
        subfield = field + "." + rule
        if subfield in self.messages:
            return self.messages.get(subfield)

        return False

    def _overwrite_errors(self):
        for field in self.messages:
            if field in self._errors and "." not in field:
                new_error = self.messages.get(field)
                formatted_error = self._format_error(
                    new_error,
                    field,
                    dict(field=field)
                )
                self._errors[field] = [formatted_error]

    def _overwrite_fields(self, fields):
        for field in fields:
            if fields.get(field) in self.fields:
                new_field_name = self.fields.get(fields.get(field))
                fields[field] = new_field_name

    def _overwrite_values(self, field, fields):
        if field in self.values:
            value_overwrites = self.values.get(field)
            for value_overwrite in value_overwrites:
                if value_overwrite in fields:
                    fields[value_overwrite] = value_overwrites.get(value_overwrite)

    def _add_error(self, rule, field, error, fields=None):
        if field not in self._errors:
            self._errors[field] = []

        overwrite = self._overwrite_error(field, rule)
        formatted_error = self._format_error(overwrite or error, field, fields)

        self._errors[field].append(formatted_error)

    def _format_error(self, error, field, fields):
        self._overwrite_fields(fields)
        self._overwrite_values(field, fields)

        return error.format(**fields)

    @staticmethod
    def valid_email(email):
        return rls.EmailRule.valid_email(email)

    @staticmethod
    def valid_url(url):
        return rls.UrlRule.valid_url(url)

    @staticmethod
    def valid_ip(ip):
        return rls.IpRule.valid_ip(ip)

    @staticmethod
    def valid_uuid4(uuid):
        return rls.Uuid4Rule.valid_uuid4(uuid)

    @staticmethod
    def valid_string(string):
        return rls.StringRule.valid_string(string)

    @staticmethod
    def valid_integer(integer):
        return rls.IntegerRule.valid_integer(integer)

    @staticmethod
    def valid_boolean(boolean):
        return rls.BooleanRule.valid_boolean(boolean)

    @staticmethod
    def valid_alpha_num(value):
        return rls.AlphaNumRule.valid_alpha_num(value)

    @staticmethod
    def valid_alpha_num_space(value):
        return rls.AlphaNumSpaceRule.valid_alpha_num_space(value)
