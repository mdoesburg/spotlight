from typing import Union, List

from spotlight import errors as err
from spotlight import rules as rls


class Validator:
    class Plugin:
        def rules(self) -> List[rls.BaseRule]:
            return []

    """
    Creates an instance of the Validator class.
    """

    def __init__(self, plugins: List[Plugin] = None):

        self._rules = None
        self._input = None
        self._errors = {}

        self.messages = {}
        self.fields = {}
        self.values = {}

        self._implicit_rules = []
        self._registered_rules = []
        self._available_rules = {}

        self._setup_default_rules()
        self._setup_plugins(plugins or [])

    def _setup_default_rules(self):
        self.register_rules(self._default_rules())

    @staticmethod
    def _default_rules() -> List[rls.BaseRule]:
        return [
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
            rls.JsonRule(),
            rls.ListRule(),
            rls.Uuid4Rule(),
            rls.AcceptedRule(),
        ]

    def _setup_rule(self, rule):
        self._available_rules[rule.name] = rule
        if rule.implicit:
            self._implicit_rules.append(rule.name)

    @staticmethod
    def _dynamically_add_static_validation_methods(rule):
        for attr in dir(rule):
            if attr.startswith("valid_"):
                validation_method = getattr(rule, attr)
                setattr(Validator, attr, staticmethod(validation_method))

    def register_rules(self, rules: [rls.BaseRule]):
        for rule in rules:
            self.register_rule(rule)

    def register_rule(self, rule: rls.BaseRule):
        self._registered_rules.append(rule)
        self._setup_rule(rule)

    def validate(
        self, input_: Union[dict, object], rules: dict, flat: bool = False
    ) -> Union[dict, list]:
        """
        Validate input with given rules.

        Parameters
        ----------
        input_ : Union[dict, object]
            Dict or object with input that needs to be validated.
            For example: {"email": "john.doe@example.com"},
            Input(email="john.doe@example.com")
        rules : Union[dict, object]
            Dict with validation rules for given input.
            For example: {"email": "required|email|unique:user,email"}
        flat : bool (default=False)
            Determines if a flat list of errors or a dict of errors should be
            returned. For example: ["error1", "error2", "error3"] vs.
            {"email": ["error1", "error2"], "password": ["error3"]}

        Returns
        ----------
        errors: Union[dict, list] (default=dict)
            Returns a dict or list of errors. Dependent on the flat flag.
        """
        self._rules = rules
        self._input = input_
        self._errors = {}

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
                    # Split rule name and rule_values
                    rule_name, *rule_values = rule.split(":")

                    # Check if field is validatable
                    if self._is_validatable(rule_name, field):
                        # Check if rule exists
                        if rule_name in self._available_rules:
                            matched_rule = self._available_rules.get(rule_name)

                            # Execute correct validation method
                            value = self._input.get(field)

                            # Rule
                            if isinstance(matched_rule, rls.Rule):
                                passed = matched_rule.passes(field, value)
                            # Dependent Rule
                            elif isinstance(matched_rule, rls.DependentRule):
                                passed = matched_rule.passes(
                                    field, value, rule_values, self._input
                                )

                            # If rule didn't pass, add error
                            if not passed:
                                self._add_error(
                                    rule_name,
                                    field,
                                    matched_rule.message(),
                                    matched_rule.message_fields,
                                )

                                # Stop validation
                                if matched_rule.stop:
                                    break
                        else:
                            raise Exception(err.RULE_NOT_FOUND.format(rule=rule_name))

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
                    new_error, field, dict(field=field)
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
            for overwrite in value_overwrites:
                if overwrite in fields:
                    fields[overwrite] = value_overwrites.get(overwrite)

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
    def valid_email(email) -> bool:
        return rls.EmailRule.valid_email(email)

    @staticmethod
    def valid_url(url) -> bool:
        return rls.UrlRule.valid_url(url)

    @staticmethod
    def valid_ip(ip) -> bool:
        return rls.IpRule.valid_ip(ip)

    @staticmethod
    def valid_uuid4(uuid) -> bool:
        return rls.Uuid4Rule.valid_uuid4(uuid)

    @staticmethod
    def valid_string(string) -> bool:
        return rls.StringRule.valid_string(string)

    @staticmethod
    def valid_integer(integer) -> bool:
        return rls.IntegerRule.valid_integer(integer)

    @staticmethod
    def valid_boolean(boolean) -> bool:
        return rls.BooleanRule.valid_boolean(boolean)

    @staticmethod
    def valid_json(value) -> bool:
        return rls.JsonRule.valid_json(value)

    @staticmethod
    def valid_alpha_num(value) -> bool:
        return rls.AlphaNumRule.valid_alpha_num(value)

    @staticmethod
    def valid_alpha_num_space(value) -> bool:
        return rls.AlphaNumSpaceRule.valid_alpha_num_space(value)

    @staticmethod
    def valid_list(value) -> bool:
        return rls.ListRule.valid_list(value)

    def _setup_plugins(self, plugins: List[Plugin]):
        for plugin in plugins:
            self.register_rules(plugin.rules())
