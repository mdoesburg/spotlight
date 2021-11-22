from typing import Union, List, overload, Tuple, Iterator, Dict, Any, Callable

from . import rules as rls, config
from .exceptions import RuleNotFoundError, InvalidDataError, InvalidRulesError
from .utils import get_field_value


Data = Union[dict, object]
ValidationFunction = Callable[..., Union[str, None]]
Rules = Dict[str, Union[str, List[Union[str, ValidationFunction]]]]


class Validator:
    """
    Creates an instance of the Validator class.

    Parameters
    ----------
    plugins : list
        A list of plugins that add additional validation rules.
    """

    class Plugin:
        """
        Creates an instance of the Validator Plugin class.
        """

        def rules(self) -> List[rls.Rule]:
            return []

    def __init__(self, plugins: List[Plugin] = None):
        self.data = None
        self.rules = None
        self.output = {}
        self.config = config
        self._flat_list = []

        self.overwrite_messages = {}
        self.overwrite_fields = {}
        self.overwrite_values = {}

        self._available_rules: Dict[str, rls.Rule] = {}

        self._setup_default_rules()
        self._setup_plugins(plugins or [])

    def _setup_default_rules(self):
        self.register_rules(self._default_rules())

    def register_rules(self, rules: [rls.Rule]):
        for rule in rules:
            self.register_rule(rule)

    def register_rule(self, rule: rls.Rule):
        self._setup_rule(rule)

    def _setup_rule(self, rule):
        self._available_rules[rule.name] = rule

    @staticmethod
    def _default_rules() -> List[rls.Rule]:
        return [
            rls.AcceptedRule(),
            rls.AfterOrEqualRule(),
            rls.AfterRule(),
            rls.AlphaNumRule(),
            rls.AlphaNumSpaceRule(),
            rls.BeforeOrEqualRule(),
            rls.BeforeRule(),
            rls.BooleanRule(),
            rls.DateTimeRule(),
            rls.DecimalRule(),
            rls.DictRule(),
            rls.EmailRule(),
            rls.EndsWithRule(),
            rls.FilledRule(),
            rls.FloatRule(),
            rls.InRule(),
            rls.IntegerRule(),
            rls.IpRule(),
            rls.JsonRule(),
            rls.ListRule(),
            rls.MaxRule(),
            rls.MinRule(),
            rls.NotWithRule(),
            rls.RegexRule(),
            rls.RequiredIfRule(),
            rls.RequiredRule(),
            rls.RequiredUnlessRule(),
            rls.RequiredWithRule(),
            rls.RequiredWithoutRule(),
            rls.SizeRule(),
            rls.StartsWithRule(),
            rls.StringRule(),
            rls.UrlRule(),
            rls.Uuid4Rule(),
        ]

    def _setup_plugins(self, plugins: List[Plugin]):
        for plugin in plugins:
            self.register_rules(plugin.rules())

    @staticmethod
    def _dynamically_add_static_validation_methods(rule):
        for attr in dir(rule):
            if attr.startswith("valid_"):
                validation_method = getattr(rule, attr)
                setattr(Validator, attr, staticmethod(validation_method))

    @overload
    def validate(
        self, data: dict, rules: Rules, flat: bool = False
    ) -> Union[dict, list]:
        ...

    @overload
    def validate(
        self, data: object, rules: Rules, flat: bool = False
    ) -> Union[dict, list]:
        ...

    def validate(
        self, data: Data, rules: Rules, flat: bool = False
    ) -> Union[dict, list]:
        """
        Validate data with given rules.

        Parameters
        ----------
        data : dict or object
            Dict or object that can be converted to a dict with data that needs
            to be validated.
            For example: {"email": "john.doe@example.com"},
            CustomDataClass(email="john.doe@example.com")
        rules : dict
            Dict with validation rules for the given data.
            For example: {"email": "required|email|unique:user,email"}
        flat : bool, optional
            Returns a list of errors instead of a dict if true.

        Returns
        -------
        errors : dict or list
            Dict or list of errors. When a dict of errors is returned, each key
            represents the field name, and the corresponding value is a list of
            errors for that key/field. When the optional parameter `flat` is
            set to true, a list of only the error messages is returned.
        """
        self.data = data
        self.rules = rules
        self.output = {}

        self._convert_data_to_dict()
        self._validate_rules_type()
        self._validate_data()

        if flat:
            self._flat_list = []
            self._flatten_output(self.output)

            return self._flat_list

        return self.output

    def _sub_fields(self, field) -> Iterator[str]:
        if not self._contains_wildcard(field):
            yield field
            return

        root = field.split(self.config.FIELD_WILD_CARD)[0].strip(
            self.config.FIELD_DELIMITER
        )
        root_value = self._get_field_value(root)

        if isinstance(root_value, list):
            for i, _ in enumerate(root_value):
                new_field = field.replace(self.config.FIELD_WILD_CARD, str(i), 1)
                yield from self._sub_fields(new_field)

    def _validate_data(self):
        # Iterate over fields
        for raw_field, rules in self._field_iterator():
            # Iterate over sub fields
            for field in self._sub_fields(raw_field):
                # Iterate over rules
                for rule, rule_parameters in self.rule_iterator(rules):
                    # Check if field is validatable
                    if self._is_validatable(field, rule):
                        value = self._get_field_value(field)
                        # If rule didn't pass, add error
                        if not rule.passes(field, value, rule_parameters, self):
                            self._add_error(rule)
                            # Stop
                            if rule.stop:
                                break

    def _field_iterator(self) -> Iterator[Tuple[str, List[str]]]:
        for field, rules in self.rules.items():
            if isinstance(rules, list):
                yield field, rules
            else:
                yield field, self._split_rules(rules)

    def rule_iterator(self, rules) -> Iterator[Tuple[rls.Rule, List[str]]]:
        for rule in rules:
            if isinstance(rule, Callable):
                yield rls._FunctionRule(rule), []
                continue

            rule_name = self._rule_name(rule)
            rule_parameters = self._rule_parameters(rule)

            if not self._rule_exists(rule_name):
                raise RuleNotFoundError(rule_name)

            rule = self._available_rules.get(rule_name)
            yield rule, rule_parameters

    def _split_rules(self, rules: str) -> List[str]:
        return rules.split(self.config.RULE_DELIMITER)

    def _rule_name(self, rule: str) -> str:
        return self._split_rule(rule)[0]

    def _rule_parameters(self, rule: str) -> List[str]:
        if self.config.RULE_PARAM_DELIMITER not in rule:
            return []

        return self._split_rule(rule)[1].split(self.config.RULE_PARAMS_DELIMITER)

    def _split_rule(self, rule: str) -> List[str]:
        return rule.split(self.config.RULE_PARAM_DELIMITER, 1)

    def _convert_data_to_dict(self):
        if not isinstance(self.data, dict):
            try:
                self.data = self.data.__dict__
            except AttributeError:
                raise InvalidDataError(type(self.data))

    def _validate_rules_type(self):
        if not isinstance(self.rules, dict):
            raise InvalidRulesError(type(self.rules))

    def _rule_exists(self, rule_name: str) -> bool:
        return rule_name in self._available_rules

    def _contains_wildcard(self, value) -> bool:
        return self.config.FIELD_WILD_CARD in value

    def _is_validatable(self, field: str, rule: rls.Rule) -> bool:
        return self._field_is_present(field) or rule.implicit

    def _field_is_present(self, field: str) -> bool:
        return self._get_field_value(field) is not None

    def _add_error(self, rule: rls.Rule):
        field = rule.message_fields.get(self.config.FIELD_KEY)
        error = self._create_error(rule)

        if field in self.output:
            self.output.get(field).append(error)
        else:
            self.output[field] = [error]

    def _create_error(self, rule: rls.Rule):
        error = rule.message
        fields = rule.message_fields
        field = fields.get(self.config.FIELD_KEY)
        field = self._convert_field_to_wildcard_field(field)
        combined_field = field + self.config.FIELD_DELIMITER + rule.name

        # Overwrite values
        fields = self._overwrite_values(field, fields)

        # If present, format values
        if "values" in fields:
            fields["values"] = self._format_values(fields["values"])

        # Overwrite messages
        error = self._overwrite_messages(error, rule.name, field, combined_field)

        # Overwrite fields
        fields = self._overwrite_fields(fields)

        return error.format(**fields)

    def _overwrite_values(self, field, fields) -> dict:
        for key in ["value", "values"]:
            new_values = fields.get(key)
            field_overwrite_values = self.overwrite_values.get(field, [])

            # Values
            if isinstance(new_values, list):
                # Field
                self._overwrite_values_in_list(
                    fields, new_values, field_overwrite_values, key
                )
                # Global
                self._overwrite_values_in_list(
                    fields, new_values, self.overwrite_values, key
                )
            # Value
            elif isinstance(new_values, str):
                # Field
                self._overwrite_value(fields, new_values, field_overwrite_values, key)
                # Global
                self._overwrite_value(fields, new_values, self.overwrite_values, key)

            # Other field
            if "other" in fields:
                other = fields.get("other")
                field_overwrite_values = self.overwrite_values.get(other, [])
                self._overwrite_value(fields, new_values, field_overwrite_values, key)

        return fields

    @staticmethod
    def _overwrite_values_in_list(fields, new_values, overwrites, key):
        for index, value in enumerate(new_values):
            if value in overwrites:
                fields[key][index] = overwrites.get(value)

    @staticmethod
    def _overwrite_value(fields, new_values, overwrites, key):
        if new_values in overwrites:
            fields[key] = overwrites.get(new_values)

    @staticmethod
    def _format_values(values: List[str]) -> str:
        return ", ".join(values)

    def _overwrite_messages(self, error, *fields):
        for field in fields:
            if field in self.overwrite_messages:
                error = self.overwrite_messages[field]

        return error

    def _overwrite_fields(self, fields):
        for overwrite_field, overwrite_value in self.overwrite_fields.items():
            for key, value in fields.items():
                value = self._convert_field_to_wildcard_field(value)
                if overwrite_field == value:
                    fields[key] = overwrite_value

        return fields

    def _convert_field_to_wildcard_field(self, field) -> str:
        split_fields = str(field).split(self.config.FIELD_DELIMITER)
        for index, field in enumerate(split_fields):
            if field.isnumeric():
                split_fields[index] = self.config.FIELD_WILD_CARD

        return self.config.FIELD_DELIMITER.join(split_fields)

    def _flatten_output(self, output: dict):
        for field, errors in output.items():
            for error in errors:
                self._flat_list.append(error)

    def _get_field_value(self, field) -> Any:
        return get_field_value(self.data, field)

    def field_rules(self, field: str) -> List[str]:
        return self._split_rules(self.rules.get(field))

    @staticmethod
    def valid_email(value: Any) -> bool:
        return rls.EmailRule.valid_email(value)

    @staticmethod
    def valid_url(value: Any) -> bool:
        return rls.UrlRule.valid_url(value)

    @staticmethod
    def valid_ip(value: Any) -> bool:
        return rls.IpRule.valid_ip(value)

    @staticmethod
    def valid_uuid4(value: Any) -> bool:
        return rls.Uuid4Rule.valid_uuid4(value)

    @staticmethod
    def valid_string(value: Any) -> bool:
        return rls.StringRule.valid_string(value)

    @staticmethod
    def valid_integer(value: Any) -> bool:
        return rls.IntegerRule.valid_integer(value)

    @staticmethod
    def valid_float(value: Any) -> bool:
        return rls.FloatRule.valid_float(value)

    @staticmethod
    def valid_decimal(value: Any) -> bool:
        return rls.DecimalRule.valid_decimal(value)

    @staticmethod
    def valid_boolean(value: Any) -> bool:
        return rls.BooleanRule.valid_boolean(value)

    @staticmethod
    def valid_json(value: Any) -> bool:
        return rls.JsonRule.valid_json(value)

    @staticmethod
    def valid_alpha_num(value: Any) -> bool:
        return rls.AlphaNumRule.valid_alpha_num(value)

    @staticmethod
    def valid_alpha_num_space(value: Any) -> bool:
        return rls.AlphaNumSpaceRule.valid_alpha_num_space(value)

    @staticmethod
    def valid_list(value: Any) -> bool:
        return rls.ListRule.valid_list(value)

    @staticmethod
    def valid_dict(value: Any) -> bool:
        return rls.DictRule.valid_dict(value)

    @staticmethod
    def valid_date_time(value: Any, date_time_format: str = None) -> bool:
        return rls.DateTimeRule.valid_date_time(value, date_time_format)
