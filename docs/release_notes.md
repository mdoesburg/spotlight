# Release Notes

## 2.1.0
### Features
- Add support for custom validation functions

## 2.0.1
### Fixes
- Add missing empty checks to the required_if, required_unless, required_with, and required_without rules. These rules were only checking if a field was present instead of also checking if the value was empty or not.

## 2.0.0
### Breaking Changes
- `True` and `False` are now considered valid integers, because bool is an instance of int in Python.

## 1.1.0
### Features
- Add regex rule
- Add decimal support to size rule