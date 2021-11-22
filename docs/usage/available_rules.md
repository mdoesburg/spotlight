# Available Rules

## accepted
The field under validation must be yes, on, 1, or true. This is useful for validating "Terms of Service" acceptance.
```
accepted
```

## after
The field under validation must be a value after a given date/time. For more details about formatting see the [date_time](#date_time) rule.
```
after:2019-12-31 12:00:00
```

If the after rule is accompanied by the date_time rule, and a non default format is specified, the specified format will be assumed for the after rule as well:
```
date_time:%H:%M:%S|after:12:00:00
```

Instead of passing a date/time string to be evaluated by the `strptime` Python function, you may specify another field to compare against the date/time:
```
after:some_field
```

## after_or_equal
The field under validation must be a value after or equal to a given date/time. For more information, see the [after](#after) rule.

## alpha_num
The field under validation must be entirely alpha-numeric characters.
```
alpha_num
```

## alpha_num_space
The field under validation may have alpha-numeric characters, as well as spaces.
```
alpha_num_space
```

## before
The field under validation must be a value before a given date/time. For more details about formatting see the [date_time](#date_time) rule.
```
before:2019-12-31 12:00:00
```

If the before rule is accompanied by the date_time rule, and a non default format is specified, the specified format will be assumed for the before rule as well:
```
date_time:%H:%M:%S|before:12:00:00
```

Instead of passing a date/time string to be evaluated by the `strptime` Python function, you may specify another field to compare against the date/time:
```
before:some_field
```

## before_or_equal
The field under validation must be a value before or equal to a given date/time. For more information, see the [before](#before) rule.

## boolean
The field under validation must be a boolean.
```
boolean
```

## date_time
The field under validation must be a valid date/time matching the "YYYY-MM-DD hh:mm:ss" format, or a custom specified format. For example, a field being validated with the following format "date_time:%m/%d/%Y" must match the "MM/DD/YYYY" format. The date/time validation uses the `strptime` Python function. For more info on valid formatting symbols check the following [Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).
```
date_time
```
```
date_time:format
```

## decimal
The field under validation must be a decimal.
```
decimal
```

## dict
The field under validation must be a dict.
```
dict
```

## email
The field under validation must be a valid email address.
```
email
```

## ends_with
The field under validation must end with one of the given values.
```
ends_with:value,other,...
```

## filled
The field under validation must not be empty when it is present.
```
filled
```

## float
The field under validation must be a float.
```
float
```

## in
The field under validation must be included in the given list of values. 
```
in:value,other,...
```

## integer
The field under validation must be an integer.
```
integer
```

Note: Since version 2.0, True and False are considered valid integers, because bool is an instance of int in Python.

## ip
The field under validation must be an IP address.
```
ip
```

## json
The field under validation must be a valid JSON string.
```
json
```

## list
The field under validation must be a list.
```
list
```

## max
The field under validation must be less than or equal to the given maximum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
max:value
```

## min
The field under validation must be greater than or equal to the given minimum value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
min:value
```

## not_with
The field under validation can't be present if the other specified field is present.
```
not_with:other
```

## regex

The field under validation must match the given regular expression. Internally, this rule uses the Python re.fullmatch() function.
```
regex:pattern
```

Note: When using the regex rule, it may be necessary to specify rules in a list instead of using pipe delimiters, especially if the regular expression contains a pipe character, like so:
```python
rules = {
    "some_field": ["required", "regex:a|b"]
}
```

## required
The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:
* The value is _None_.
* The value is an empty string.
* The value is an empty list.
```
required
```

## required_if
The field under validation must be present and not empty if the other specified field equals a certain value.
```
required_if:other,value
```

## required_unless
The field under validation must be present and not empty unless the other specified field equals a certain value.
```
required_unless:other,value
```

## required_with
The field under validation must be present and not empty only if any of the other specified fields are present.
```
required_with:field1,field2,...
```

## required_without
The field under validation must be present and not empty only when any of the other specified fields are not present.
```
required_without:field1,field2,...
```

## size
The field under validation must have a size matching the given value. For strings, value corresponds to the number of characters. For integers, value corresponds to a given integer value. For floats, value corresponds to a given float value. For decimals, value corresponds to a given decimal value. For lists and dicts, value corresponds to the length of the list/dict.
```
size:value
```

## starts_with
The field under validation must start with one of the given values.
```
starts_with:value,other,...
```

## string
The field under validation must be a string.
```
string
```

## url
The field under validation must be a valid URL.
```
url
```

## uuid4
The field under validation must be a valid uuid (version 4).
```
uuid4
```