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

    @reactive.hook('{peers:storpool-service}-relation-joined')
    def peer_joined(self):
        """
        Let the main charm handle data received from the other units.
        """
        rdebug('relation-joined invoked')
        self.set_state('{relation_name}.notify')
        self.set_state('{relation_name}.notify-joined')

    @reactive.hook('{peers:storpool-service}-relation-{changed,departed,broken}')
    def peer_changed(self):
        """
        Let the main charm handle data received from the other units.
        """
        rdebug('relation-changed/departed/broken invoked')
        self.set_state('{relation_name}.notify')
