"""

This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Sep 26, 2014.
"""
from pkg_resources import resource_filename # pylint: disable=E0611
from pyramid.renderers import render_to_response
import pytest

from everest.tests.fixtures import ResourceCreatorContextManager
import re
import os


__docformat__ = 'reStructuredText en'
__all__ = []

pytest_plugins = 'telex.tests.conftest'


@pytest.yield_fixture
def telex_rgg(class_ini, class_configurator):
    with ResourceCreatorContextManager(class_ini, class_configurator) as repo:
        yield repo


@pytest.mark.usefixtures('telex_rgg')
class TestRenderer(object):
    package_name = 'telex_rgg.tests'
    config_file_name = resource_filename('telex.tests', 'configure.zcml')

    def test_rgg(self, cmd_def_collection):
        rsp = render_to_response('rgg', dict(context=cmd_def_collection))
        assert not rsp is None
        # Parse out and check the rgg script.
        pat = re.compile('.*<rgg>(.+)</rgg>', flags=re.DOTALL)
        match = pat.search(rsp.body)
        assert not match is None
        grp = match.groups()[0]
        lines = [line.strip()
                 for line in grp.split(os.linesep) if not line.strip() == '']
        assert len(lines) == 4
        assert lines[0].split('=')[0].strip() == '__jsonclass__'
        assert lines[1].split('=')[0].strip() == 'submitter'
        assert lines[2].split('=')[0].strip() == 'command_definition'
        assert lines[3].split('=')[0].strip() == 'parameters.text'
