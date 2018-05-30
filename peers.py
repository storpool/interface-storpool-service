"""
A Juju charm interface that helps the `storpool-block` charm keep track of
which units have been installed and configured.
"""
from charms import reactive

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
        Let the main charm handle data received from the other units.
        """
        rdebug('relation-joined/changed invoked')
        self.set_state('{relation_name}.present')
        self.set_state('{relation_name}.notify')

    @reactive.hook('{peers:storpool-service}-relation-{departed,broken}')
    def peer_gone(self):
        """
        Let the main charm know that our peers have left the building.
        """
        rdebug('relation-departed/broken invoked')
        self.remove_state('{relation_name}.present')
        self.remove_state('{relation_name}.notify')
