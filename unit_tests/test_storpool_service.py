#!/usr/bin/python3

"""
A set of unit tests for the storpool-service interface.
"""

import os
import sys
import unittest

import mock

root_path = os.path.realpath('.')
if root_path not in sys.path:
    sys.path.insert(0, root_path)

lib_path = os.path.realpath('unit_tests/lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from spcharms import utils as sputils


import peers as testee


class TestStorPoolService(unittest.TestCase):
    """
    Test the data exchanged by the storpool-service interface.
    """

    def get_call_count(self, obj):
        """
        Fetch the current call count of the tools used.
        """
        return {
            'rdebug': sputils.rdebug.call_count,
            'remove': obj.remove_state.call_count,
            'set': obj.set_state.call_count,
        }

    def check_update_call_count(self, obj, ref, delta):
        """
        Fetch the current call count and check that the delta is
        the same as the expected one.
        """
        current = self.get_call_count(obj)
        for (k, v) in delta.items():
            ref[k] += v
        self.assertEqual(current, ref)

    def test_service(self):
        """
        Test the data exchanged by the provides interface.
        """
        obj = testee.StorPoolServicePeer('storpool-service:42')
        obj.set_state = mock.Mock()
        obj.remove_state = mock.Mock()
        call_c = self.get_call_count(obj)

        obj.peer_joined()
        self.check_update_call_count(obj, call_c, {
            'rdebug': 1,
            'set': 2,
        })

        obj.peer_changed()
        self.check_update_call_count(obj, call_c, {
            'rdebug': 1,
            'set': 1,
        })
