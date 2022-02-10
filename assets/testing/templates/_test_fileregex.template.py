# -*- coding: utf-8 -*-
# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_fileregex

POINTS = ${points}

def test_${name}(pattern=r'${fileregex}'):
    return _test_fileregex(pattern)


