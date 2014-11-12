"""
This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Sep 26, 2014.
"""
import os
import re

from pkg_resources import resource_filename # pylint: disable=E0611
from pyramid.renderers import render_to_response
import pytest

from everest.resources.utils import get_root_collection
from telex.constants import VALUE_TYPES
from telex.interfaces import IShellCommandDefinition
import xml.etree.ElementTree as et


__docformat__ = 'reStructuredText en'
__all__ = ['TestRenderer',
           ]


@pytest.mark.usefixtures('resource_repo')
class TestRenderer(object):
    package_name = 'telex_rgg.tests'
    config_file_name = resource_filename('telex.tests', 'configure.zcml')

    def test_rgg_default(self):
        coll = get_root_collection(IShellCommandDefinition)
        rsp = render_to_response('rgg', dict(context=coll))
        assert rsp.body.find('New telex Command Definition') != -1
        for vt in VALUE_TYPES:
            assert rsp.body.find('New %s telex Parameter Definit' % vt) != -1

    def test_rgg_echo(self, cmd_def_echo):
        rsp = render_to_response('rgg', dict(context=cmd_def_echo.__parent__))
        lines = self.__extract_rgg_tag_from_response(rsp)
        assert len(lines) == 9
        assert lines[1].split('=')[0].strip() == '__jsonclass__'
        assert lines[2].split('=')[0].strip() == 'submitter'
        assert lines[3].split('=')[0].strip() == 'command_definition'
        assert lines[4].split('=')[0].strip() == \
                                  'parameters.item#1.__jsonclass__'
        assert lines[5].split('=')[0].strip() == \
                                    'parameters.item#1.parameter_definition'
        assert lines[6].split('=')[0].strip() == \
                                    'parameters.item#1.value'

    @pytest.mark.parametrize('prm_def_args,prm_opts_args,exp',
                             [(('int', 'Integer', VALUE_TYPES.INT),
                               [('entry_width', 35)],
                               ('textfield',
                                {'label':'Integer', 'size':'35',
                                 'data-type':'number',
                                 'knime-data-type':'int'})),
                              (('double', 'Double', VALUE_TYPES.DOUBLE),
                               [('entry_width', 36)],
                               ('textfield',
                                {'label':'Double', 'size':'36',
                                 'data-type':'number',
                                 'knime-data-type':'double'})),
                              (('bool', 'Boolean', VALUE_TYPES.BOOLEAN),
                               [],
                               ('checkbox',
                                {'label':'Boolean',
                                 'knime-data-type':'bool'})),
                              (('timestamp', 'Timestamp',
                                VALUE_TYPES.DATETIME),
                               [],
                               ('textfield',
                                {'label':'Timestamp', 'size':'30'})),
                              (('file', 'File', VALUE_TYPES.FILE),
                               [('extensions', 'txt,csv')],
                               ('filechooser',
                                {'label':'File',
                                 'accepted-extensions':'txt,csv'})),
                              (('string', 'String', VALUE_TYPES.STRING),
                               [('choices', 'foo,bar')],
                               ('combobox',
                                {'label':'String', 'items':'foo,bar'})),
                              (('string', 'String', VALUE_TYPES.STRING),
                               [('choices', 'http://myentries')],
                               ('combobox',
                                {'label':'String',
                                 'items':'$$$URL(http://myentries)$$$'})),
                              (('string', 'String', VALUE_TYPES.STRING),
                               [('choices', 'http://myentries'),
                                ('choices_value_attribute', 'id')],
                               ('combobox',
                                {'label':'String',
                                 'items':'$$$URL(http://myentries, id)$$$'})),
                              (('string', 'String', VALUE_TYPES.STRING),
                               [('choices', 'http://myentries'),
                                ('choices_value_attribute', 'id'),
                                ('choices_label_attribute', 'label')],
                               ('combobox',
                                {'label':'String',
                                 'items':
                                  '$$$URL(http://myentries, id, label)$$$'})),
                              ]
                             )
    def test_rgg_all_value_types(self, cmd_def_empty_entity, prm_def_args,
                                 prm_opts_args, exp):
        pd = cmd_def_empty_entity.add_parameter_definition(*prm_def_args)
        for prm_opt_args in prm_opts_args:
            pd.add_parameter_option(*prm_opt_args)
        coll = get_root_collection(IShellCommandDefinition)
        coll.create_member(cmd_def_empty_entity)
        rsp = render_to_response('rgg', dict(context=coll))
        lines = self.__extract_rgg_tag_from_response(rsp)
        xml_string = ' '.join(lines[6:]).split('=', 1)[1].strip()
        el = et.fromstring(xml_string)
        assert el.tag == exp[0]
        assert el.attrib == exp[1]

    def __extract_rgg_tag_from_response(self, response):
        # Parse out the rgg script.
        assert not response is None
        pat = re.compile('<rgg>(.+?)</rgg>', flags=re.DOTALL)
        rgg_string = pat.findall(response.body)[-1]
        return [line.strip()
                for line in rgg_string.split(os.linesep)
                if not line.strip() == '']
