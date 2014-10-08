"""
This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Sep 25, 2014.
"""
from everest.interfaces import IMime
from everest.mime import register_mime_type
from everest.resources.utils import get_collection_class
from telex.interfaces import ICommandDefinition
from zope.interface import provider # pylint: disable=E0611,F0401

from .renderers import RggRenderer
from pyramid.threadlocal import get_current_registry


class IRggScriptMime(IMime):
    """Marker interface for RGG script mime type."""


@provider(IRggScriptMime)
class RggScriptMime(object):
    mime_type_string = 'text/x-script.rgg'
    file_extension = '.rgg'

RGG_SCRIPT_MIME = RggScriptMime.mime_type_string



def load_plugin(config):
    #
#    register_mime_type(RggScriptMime)
    #
    config.add_renderer('rgg', RggRenderer)
    config.add_collection_view(ICommandDefinition,
                               renderer='rgg',
                               name='rgg'
                               )
