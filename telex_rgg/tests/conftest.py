"""
This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Oct 16, 2014.
"""
import pytest

from telex.entities import ShellCommandDefinition
from telex.tests import conftest as telex_conftest


__docformat__ = 'reStructuredText en'
__all__ = []


# For some reason, the pytest_plugins mechanism does not work here, so
# we import the needed test fixtures manually.
cmd_def_echo = telex_conftest.shell_cmd_def_echo
submitter = telex_conftest.submitter

@pytest.fixture
def cmd_def_empty_entity(submitter): # pylint:disable=W0621
    return ShellCommandDefinition('value_type_test',
                                  'Command testing rendering of value types',
                                  'foo',
                                  submitter,
                                  )
