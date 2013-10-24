#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @author: jiakuanwang
#

import Queue
import logging
import os
import time
import util.thread_util as thread_util

if os.name == "posix":
    from Cocoa import *
    from Foundation import *

event_queue = Queue.Queue(0)

GAP_TIME = 1000  # In milliseconds
lastCheck = int(time.time() * 1000)

class EventHandlingThread(thread_util.StoppableThread):
    def __init__(self):
        self.__queue = event_queue
        super(EventHandlingThread, self).__init__()

    def run(self):
        while not self.stopped():
            item = None
            try:
                item = self.__queue.get_nowait()
            except Queue.Empty:
                # Ignore empty
                pass

            if item is None:
                # sleep 500 ms
                self.wait(0.5)
                continue

            print 'Received an event'


class MacOSXEventMonitor():
    def init(self):
        print "Initializing events monitor for Mac OS X..."
        # self.pool = NSAutoreleasePool.alloc().init()
        self._observer = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
            NSLeftMouseDownMask
            | NSLeftMouseUpMask
            | NSRightMouseDownMask
            | NSRightMouseUpMask
            | NSMouseMovedMask
            | NSLeftMouseDraggedMask
            | NSRightMouseDraggedMask
            | NSMouseEnteredMask
            | NSMouseExitedMask
            | NSScrollWheelMask
            | NSKeyDownMask
            | NSKeyUpMask
            | NSControlKeyMask
            | NSAlternateKeyMask
            | NSCommandKeyMask
            | NSFlagsChangedMask, self.handleEvent)

    def handleEvent(self, event):
        # NSLog(u"%@", event)
        # flags = event.modifierFlags()
        # modifiers = []  # OS X api doesn't care it if is left or right
        # if (flags & NSControlKeyMask):
        #     modifiers.append('CONTROL')
        # if (flags & NSAlternateKeyMask):
        #     modifiers.append('ALTERNATE')
        # if (flags & NSCommandKeyMask):
        #     modifiers.append('COMMAND')
        # NSLog(u"%@", modifiers)

        currTime = int(time.time() * 1000)
        if currTime - lastCheck > GAP_TIME:
            event_queue.put(1)

    def stop(self):
        NSEvent.removeMonitor_(self._observer)
