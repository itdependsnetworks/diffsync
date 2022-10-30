"""Utility functions for DiffSync library.

Copyright (c) 2020-2021 Network To Code, LLC <info@networktocode.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import OrderedDict
from typing import List

SPACE = "    "
BRANCH = "│   "
TEE = "├── "
LAST = "└── "


def intersection(lst1, lst2) -> List:
    """Calculate the intersection of two lists, with ordering based on the first list."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def symmetric_difference(lst1, lst2) -> List:
    """Calculate the symmetric difference of two lists."""
    return sorted(set(lst1) ^ set(lst2))


class OrderedDefaultDict(OrderedDict):
    """A combination of collections.OrderedDict and collections.DefaultDict behavior."""

    def __init__(self, dict_type):
        """Create a new OrderedDefaultDict."""
        self.factory = dict_type
        super().__init__(self)

    def __missing__(self, key):
        """When trying to access a nonexistent key, initialize the key value based on the internal factory."""
        self[key] = value = self.factory()
        return value


# from: https://stackoverflow.com/questions/72618673/list-directory-tree-structure-in-python-from-a-list-of-path-file
def _tree(data: dict, prefix: str = ""):
    """Given a dictionary will yield a visual tree structure.

    A recursive generator, given a dictionary will yield a visual tree structure line by line
    with each line prefixed by the same characters.
    """
    # contents each get pointers that are ├── with a final └── :
    pointers = [TEE] * (len(data) - 1) + [LAST]
    for pointer, path in zip(pointers, data):
        yield prefix + pointer + path
        if isinstance(data[path], dict):  # extend the prefix and recurse:
            extension = BRANCH if pointer == TEE else SPACE
            # i.e. SPACE because LAST, └── , above so no more |
            yield from _tree(data[path], prefix=prefix + extension)


def tree_string(data: dict, root):
    """String wrapper around `_tree` function to add header and provide tree view of a dictionary."""
    output = root
    for line in _tree(data):
        output = output + "\n" + line
    return output


def set_key(data, keys):
    """Set a nested dictionary key given a set of keys."""
    current_level = data
    for item in keys:
        if item not in current_level:
            current_level[item] = {}
        current_level = current_level[item]


def get_path(nested_dict, search_value):
    """Find the path of keys in a dictionary, given a single unique value."""
    for key in nested_dict.keys():
        if key == search_value:
            return [key]
        if isinstance(nested_dict[key], dict):
            path = get_path(nested_dict[key], search_value)
            if path is not None:
                return [key] + path
    return None
