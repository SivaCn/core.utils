# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import pickle

from typing import Optional
from string import Template
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import UTC, datetime, timedelta, date

from types import SimpleNamespace
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import yaml
import simplejson as json
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.frozenobj import (
    DictProxy,
    ListProxy,
    SetProxy
)

from core.utils.helpers.date import (
    parse_datetime_from_iso,
    parse_date_from_iso,
)
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def read_yaml(yaml_file: str) -> str:
    """Reads a given yaml file and returns python dictionary."""

    data = None

    with open(yaml_file, 'r') as stream:
        try:
            data = yaml.safe_load(stream)

        except yaml.YAMLError:
            raise Exception(f"Unable to read the supplied yaml file '{yaml_file}'")

    return data


def string_substitute(text: str, substitutes: dict) -> str:
    return Template(text).safe_substitute(substitutes)


def pickle_file_serialize(file_path: str, data: dict) -> None:

    with open(file_path, 'wb') as fd:
        #
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, fd, pickle.HIGHEST_PROTOCOL)


def pickle_file_deserialize(file_path: str) -> dict:

    data = None

    with open(file_path, 'rb') as fd:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(fd)

    return data


def py_datatype_from_str(value: str):

    """Parses and applies auto casting when possible.
    """

    def auto_cast(value):

        value = value.strip()

        if '.' in value:
            try:
                return float(value)
            except Exception:
                pass

        if value.isdigit():
            return int(value)

        if value.lower() == 'true':
            return True

        if value.lower() == 'false':
            return False

        return value

    values = [auto_cast(item) for item in value.strip().split(',')]

    return values[0] if len(values) == 1 else values


class DotDict:
    """Simple Recursive namespace entity.

    Returns:
        Value if the key exists else None

    Usage:
        >>> nested_dict = {
        ...     'person': {
        ...         'name': 'Alice',
        ...         'age': 30,
        ...         'address': {
        ...             'street': '123 Main St',
        ...             'city': 'Anytown'
        ...         }
        ...     },
        ...     'grades': {
        ...         'Math': 90,
        ...         'Science': 85
        ...     }
        ... }

        >>> dot_accessible = DotDict(nested_dict)
        >>> dot_accessible.person.name
        'Alice'
        >>> dot_accessible.person.address.city
        'Anytown'
        >>> dot_accessible.grades.Math
        90
        >>> dot_accessible.person.hobbies  # Returns None
    """

    def __init__(self, dictionary=None):

        dictionary = dictionary or dict()

        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    #
                    # Recursively convert nested dictionaries
                    value = DotDict(value)

                elif isinstance(value, list):
                    #
                    # Convert Dicts inside the list
                    value = [DotDict(item) if isinstance(item, dict) else item for item in value]

                setattr(self, key, value)

        elif isinstance(dictionary, list):
            #
            # If the input is a list, convert each item
            self.items = [DotDict(item) if isinstance(item, dict) else item for item in dictionary]

    def __getattr__(self, item):
        #
        # Provide a safe way to access attributes
        try:
            return self.__dict__[item]
        except KeyError:
            #
            # Return None if the attribute does not exist
            return None

    def as_dict(self):
        """Convert the DotDict back to a regular dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DotDict):
                #
                # Recursively convert DotDicts back to dicts
                result[key] = value.as_dict()

            elif isinstance(value, list):
                #
                # Handle lists of DotDicts
                result[key] = [item.as_dict() if isinstance(item, DotDict) else item for item in value]

            else:
                result[key] = value

        return result

    def __repr__(self):
        arg_set = ', '.join([f'{k}: {v}' for k, v in self.__dict__.items()][:3]) + ', ...'
        return f"<{self.__class__.__name__}({arg_set})>"


def create_blackboard():
    """Create blackboard Namespace as carrier.

    Usage:
        >>> blackboard = create_blackboard()
        >>> blackboard
        SafeNamespace()
        >>> blackboard.unknown
        >>> blackboard.unknown = 'assigned'
        >>> blackboard.unknown
        'assigned'

    """
    class SafeNamespace(SimpleNamespace):
        def __getattr__(self, name):
            #
            # Return None if the attribute does not exist
            return None

    return SafeNamespace()


def get_unique_id(prefix: str='') -> str:
    """Creates an unique id (uuid) with specified prefix if any.
    """

    return f"{prefix + ':' if prefix else ''}{uuid4().__str__()}"


def sliced_uuid(uuid_str: Optional[str]=None, index: int=0) -> str:
    """."""
    if not uuid_str:
        uuid_str = str(uuid4())

    index = index or 0

    return uuid_str.split('-')[index]


def json_custom_serializer(value):

    """A customized serializer for the JSON.

    Usage:
        >>> import simplejson as json
        >>> from datetime import datetime
        >>>
        >>> data = {'date': datetime.now(UTC)}
        >>> json.dumps(data)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/usr/lib/python3.6/json/__init__.py", line 231, in dumps
            return _default_encoder.encode(obj)
          File "/usr/lib/python3.6/json/encoder.py", line 199, in encode
            chunks = self.iterencode(o, _one_shot=True)
          File "/usr/lib/python3.6/json/encoder.py", line 257, in iterencode
            return _iterencode(o, 0)
          File "/usr/lib/python3.6/json/encoder.py", line 180, in default
            o.__class__.__name__)
        TypeError: Object of type 'datetime' is not JSON serializable

        >>> json.dumps(data, default=json_custom_serializer)
        {'date': '2021-04-07T13:20:16.146518'}
    """
    if isinstance(value, UUID):
        #
        # Serialize any uuid by stringifying them
        return value.__str__()

    if isinstance(value, datetime):
        #
        # Serialize any datetime object by stringifying them
        return parse_datetime_from_iso(value.isoformat())

    if isinstance(value, date):
        #
        # Serialize any datetime object by stringifying them
        return parse_date_from_iso(value.isoformat())

    if isinstance(value, timedelta):
        #
        # Serialize the timedelta objects by stringifying them
        return value.__str__()

    if isinstance(value, Decimal):
        #
        # Serialize any Decimal object by converting it to float with 2 decimal places precision
        return round(float(value), 2)

    if isinstance(value, ListProxy):
        #
        # If the value is a ListProxy object, convert it to a list
        return list(value)

    if isinstance(value, DictProxy):
        #
        # If the value is a DictProxy object, convert it to a dictionary
        return dict(value)

    if isinstance(value, SetProxy):
        #
        # If the value is a SetProxy object, convert it to a set
        return set(value)


def json_serialize(value: list | str, sort_keys: bool=False) -> str:
    """An utility to serialize Python data into json.

    Args:
        value (str): value to be JSON serialized
        sort_keys (bool): flag to sort the keys of a given dictionary

    Note:
        1. when argument sort_keys is set to ``True`` then the ordder of keys in the result dictionary will be changed
            so use this flag wisely.

    Returns:
        ``str`` the serialized value
    """

    if not isinstance(value, (dict, list)):
        raise NotImplementedError(
            f"Serialization for the datatype: '{type(value).__class__.__name__}', is not implemented"
        )

    return json.dumps(value, default=json_custom_serializer, sort_keys=sort_keys)


def json_deserialize(value: str) -> dict | list:
    """An utility to deserialize the JSON into python data.

    Args:
        value (str): value to be deserialized

    Returns:
        Deserialized ``list`` | ``dict`` data
    """

    if not isinstance(value, str):
        raise ValueError(f'Expecting argument value of type string, Got {type(value).__class__.__name__}')

    return json.loads(value)


def json_safe(value: list | str, sort_keys: bool=False):
    """An utility to make the date JSON safe."""

    return json_deserialize(json_serialize(value, sort_keys=sort_keys))


def update_nested_dict(original: dict, updates: dict) -> dict:
    """Update a deeply nested dictionary with another one.

    Notes:
        * The function iterates through each key-value pair in the updates dictionary.
        * If both the original and updates dictionaries contain the same key and its value is also a dictionary,
            it calls itself recursively to merge those nested dictionaries.
        * If the key does not exist in original or if the values are not both dictionaries,
            it simply updates or adds the value from updates.

    """
    for key, value in updates.items():
        if isinstance(value, dict) and key in original and isinstance(original[key], dict):
            # If both original and updates have the key and it's a dictionary, recurse
            update_nested_dict(original[key], value)

        else:
            # Otherwise, update or add the value from updates
            original[key] = value

    return original
