# -*- coding: utf-8 -*-
# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_file

FILENAME = '${filename}'
POINTS = ${points}

def test_${name}():
    return _test_file(FILENAME)


