#!/usr/bin/python3

"""
A set of unit tests for the storpool-service interface.
"""

import os
import sys
import testtools

import json
import mock

from charms import reactive

root_path = os.path.realpath('.')
if root_path not in sys.path:
    sys.path.insert(0, root_path)

lib_path = os.path.realpath('unit_tests/lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from spcharms import service_hook

import peers as testee


class TestStorPoolService(testtools.TestCase):
    """
    Test the data exchanged by the storpool-presence interface.
    """

    def record_handled(self, *args):
        """
        Record a single invocation of service_hook.handled().
        """
        self.handled.append(args)

    def test_peer_departed(self):
        """
        Test that the provider interface sets a reactive state.
        """
        obj = testee.StorPoolServicePeer('here-we-are:17')

        service_hook.clear_data()
        obj.peer_departed()
        self.assertEquals([(obj, False, None, testee.rdebug)],
                          service_hook.get_data())

        # That's all, folks!

    @mock.patch('peers.StorPoolServicePeer.set_state')
    @mock.patch('peers.StorPoolServicePeer.conversation')
    def test_peer_changed(self, req_conv, set_state):
        """
        Test that the requires interface tries to exchange data.
        """
        def set_remote_state(name, value):
            """
            Record all the invocations of conv.set_state() by the charm.
            """
            self.remote_state.append((name, value))

        conv = mock.MagicMock(spec=reactive.relations.Conversation)
        conv.set_remote.side_effect = set_remote_state
        req_conv.return_value = conv

        obj = testee.StorPoolServicePeer('here-we-are:18')

        # No remote data the first time, we send our own.
        # (make sure we include a "-local" key there...)
        self.remote_state = []
        conv.get_remote.return_value = None
        obj.peer_changed()
        self.assertEquals([], service_hook.get_data())
        self.assertEquals([('storpool_service', '"me!"')], self.remote_state)

        # Okay then, let's send some data from the other side...
        # ...but with no change, so no data sent back out.
        self.remote_state = []
        conv.get_remote.return_value = json.dumps({'no': 'matter'})
        service_hook.clear_data()
        service_hook.set_changed(False)
        obj.peer_changed()
        self.assertEquals([(obj, True, {'no': 'matter'}, testee.rdebug)],
                          service_hook.get_data())
        self.assertEquals([], self.remote_state)

        # Right, so let's send some data back out now.
        self.remote_state = []
        conv.get_remote.return_value = json.dumps({'1': 2})
        service_hook.clear_data()
        service_hook.set_changed(True)
        obj.peer_changed()
        self.assertEquals([(obj, True, {'1': 2}, testee.rdebug)],
                          service_hook.get_data())
        self.assertEquals([('storpool_service', '"me!"')], self.remote_state)
