"""Module of reusable and extendable data validators. Adapted from Raymond Hettingers modern Python course.

The Validator base class, as well as the OneOf, String and Integer validators are licensed under the
following licence:

    MIT License

    Copyright (c) 2017 Raymond Hettinger

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

from abc import ABC, abstractmethod
import re


class Validator(ABC):
    """Base class for validation. Sets private attribute and validates it."""

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    """Validates if value is a set of provided options."""

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(
                f"{value!r} not a valid option.  should be one of: {self.options}"
            )


class String(Validator):
    """Validates if value is a string of a certain size."""

    def __init__(self, minsize=0, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if value is None:
            raise ValueError(f"Field '{self.private_name[1:]}' is missing.")
        if not isinstance(value, str):
            raise ValueError(f"Expected a str for '{self.private_name[1:]}'.")
        if len(value) < self.minsize:
            raise ValueError(
                f"String is too short, must be at least {self.minsize} long"
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f"String is too long, must be no bigger than {self.maxsize} long"
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f"Expected {value} to be true for {self.predicate !r}")


class Boolean(Validator):
    """Validates if value is a boolean."""

    def __set__(self, obj, value):
        self.validate(value)
        if value is False:
            value = "FALSE"
        if value is True:
            value = "TRUE"
        setattr(obj, self.private_name, value)

    def validate(self, value):
        if value is None:
            raise ValueError(f"Field '{self.private_name[1:]}' is missing.")
        if not isinstance(value, bool) and value not in ["TRUE", "FALSE"]:
            raise ValueError(f"Expected a boolean for '{self.private_name[1:]}'.")


class Integer(Validator):
    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if value is None:
            raise ValueError(f"Field '{self.private_name.split('_')[-1]}' is missing.")
        if not isinstance(value, int):
            raise ValueError(f"Expected an int for '{self.private_name[1:]}'.")
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f"{value} is too small.  Must be at least {self.minvalue}."
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f"{value} is too big.  Must be no more than {self.maxvalue}."
            )


class Numeric(Validator):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Variant Price must be either int or float")


class Regex(Validator):
    """Validates if value is matched by regex"""

    def __init__(self, regex, error_message=None):
        self.regex = re.compile(regex)
        self.error_message = (
            error_message
            or f"Value for {self.private_name[1:]} is not matched by provided regex {self.regex.pattern}"
        )

    def validate(self, value):
        if value is None:
            raise ValueError(f"Field '{self.private_name[1:]}' is missing.")
        if not isinstance(value, str):
            raise ValueError(f"Expected a str for '{self.private_name[1:]}'.")
        if not self.regex.match(value):
            raise ValueError(self.error_message)


class Image(Validator):
    """Upload images should not have _thumb, _small, or _medium suffixes in their names."""

    def validate(self, value):
        if not isinstance(value, str):
            if value is None:
                raise ValueError(f"Field '{self.private_name[1:]}' is missing.")
            if not isinstance(value, str):
                raise ValueError(f"Expected a str for '{self.private_name[1:]}'.")
        for wrong_ending in ["_thumb", "_small", "_medium"]:
            if value.endswith(wrong_ending):
                raise ValueError(
                    f"Field '{self.private_name[1:]} should not end with {wrong_ending}"
                )


class Tags(Validator):
    def __set__(self, obj, value):
        self.validate(value)
        if type(value) == list:
            value = ",".join(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        if not isinstance(value, (str, list)):
            raise ValueError("Tags must be list or string.")


class NoWhitespace(Validator):
    def validate(self, value):
        if not isinstance(value, str):
            if value is None:
                raise ValueError(f"Field '{self.private_name[1:]}' is missing.")
        if not isinstance(value, str):
            raise ValueError(f"Expected a str for '{self.private_name[1:]}'.")
        if " " in value:
            raise ValueError("Variant Fulfillment Service cannot contain spaces")
