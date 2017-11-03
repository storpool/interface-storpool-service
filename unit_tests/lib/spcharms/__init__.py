#!/usr/bin/python

import mock


class SPServiceHook(object):
    """
    Trivially simulate the service_hook utility helper with
    none of its actual functionality, just record all the calls
    to the handle() method.
    """
    def __init__(self):
        """
        Initialize an object with no recorded calls.
        """
        self.data = []
        self.changed = False

    def handle(self, obj, attaching, data, rdebug):
        """
        Record the arguments passed to the method.
        """
        self.data.append((obj, attaching, data, rdebug))
        return self.changed

    def get_data(self):
        """
        Return the recorded data.
        """
        return list(self.data)

    def clear_data(self):
        """
        Clear the recorded data for a new test.
        """
        self.data = []

    def get_state(self):
        """
        Mock the service_hook's object state dictionary and its "changed" flag.
        """
        return ({'-local': 'me!'}, self.changed)

    def set_changed(self, changed):
        """
        Set the "changed" flag for the later get_state() invocations.
        """
        self.changed = changed


utils = mock.Mock()

service_hook = SPServiceHook()
