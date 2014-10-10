"""

This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Sep 26, 2014.
"""
from urlparse import urlparse

from mako.template import Template
from pkg_resources import resource_filename # pylint: disable=E0611
from pyramid.interfaces import IRenderer

from everest.resources.utils import resource_to_url
from telex.constants import VALUE_TYPES
from zope.interface import implementer # pylint: disable=E0611,F0401
from telex.constants import ParameterOptionRegistry


__docformat__ = 'reStructuredText en'
__all__ = ['RggRenderer',
           ]


@implementer(IRenderer)
class RggRenderer(object):
    def __init__(self, info):
        self.__info = info

    def __call__(self, value, system):
        # The "context" argument is reserved in mako.
        ctxt = value.pop('context')
        value['commands'] = ctxt
        value['resource_to_url'] = resource_to_url
        value['VALUE_TYPES'] = VALUE_TYPES
        value['urlparse'] = urlparse
        value['get_options'] = ParameterOptionRegistry.get
        fn = resource_filename('telex_rgg', 'cmds.mak')
        return Template(filename=fn).render(**value)
