"""
A Juju charm interface that helps the `storpool-block` charm keep track of
which units have been installed and configured.
"""
import json

from charms import reactive

from spcharms import service_hook
from spcharms import utils as sputils


def rdebug(s):
    """
    Pass the diagnostic message string `s` to the central diagnostic logger.
    """
    sputils.rdebug(s, prefix='storpool-service')


class StorPoolServicePeer(reactive.RelationBase):
    """
    The Juju interface class that keeps track of presence data received from
    the other `storpool-block` units.
    """
    scope = reactive.scopes.UNIT

    @reactive.hook('{peers:storpool-service}-relation-{joined,changed}')
    def peer_changed(self):
        """
        Handle data received from the other units.
        """
        rdebug('relation-joined/changed invoked')
        service_hook.handle_remote_presence(self, rdebug=rdebug)

    # TODO: handle unit shutdown in a completely different way elsewhere
    @reactive.hook('{peers:storpool-service}-relation-{departed,broken}')
    def peer_gone(self):
        """
        Our peers have left the building.
        """
        rdebug('relation-departed/broken invoked')
        self.remove_state('{relation_name}.notify')
