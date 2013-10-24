#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @author: jiakuanwang
#

import threading

class Synchronized:
    #
    # As a decorator for sychronized methods.
    #

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        lock = threading.RLock()
        lock.acquire()
        try:
            result = self.func(*args)
            # Return the result
            return result
        finally:
            lock.release()

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def wait(self, seconds):
        self._stop.wait(seconds)
