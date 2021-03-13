# -*- coding: utf-8 -*-
# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_variable

FILENAME = '${filename}'
POINTS = ${points}

def test_${name}():
    return _test_variable("${variable}", ${reference},
                          FILENAME,
                          check_type=${check_type},
                          rtol=${relative_tolerance},
                          atol=${absolute_tolerance},
                          )
