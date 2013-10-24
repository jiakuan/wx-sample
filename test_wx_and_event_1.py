"""PyObjC keylogger for Python
by  ljos https://github.com/ljos
"""

from Cocoa import *
from Foundation import *
import icons
import time
import wx
import wx.lib.embeddedimage
# from PyObjCTools import AppHelper


class DemoTaskBarIcon(wx.TaskBarIcon):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE = wx.NewId()
    TBMENU_CHANGE = wx.NewId()
    TBMENU_REMOVE = wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame

        # Set the image
        icon = self.MakeIcon(icons.sample.GetImage())
        self.SetIcon(icon, "wxPython Sample")
        self.imgidx = 1

        # bind some events
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

    def CreatePopupMenu(self):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, "Restore wxPython Sample")
        menu.Append(self.TBMENU_CLOSE, "Close wxPython Sample")
        return menu


    def MakeIcon(self, img):
        """
        The various platforms have different requirements for the
        icon size...
        """
        if "wxMSW" in wx.PlatformInfo:
            img = img.Scale(16, 16)
        elif "wxGTK" in wx.PlatformInfo:
            img = img.Scale(22, 22)

        # wxMac can be any size upto 128x128, so leave the source img alone....
        icon = wx.IconFromBitmap(img.ConvertToBitmap())
        return icon

    def OnTaskBarActivate(self, evt):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()


    def OnTaskBarClose(self, evt):
        wx.CallAfter(self.frame.Close)


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Hello World")
        self.tbicon = DemoTaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.tbicon.Destroy()
        evt.Skip()


def handler(event):
    NSLog(u"%@", event)

    flags = event.modifierFlags()
    modifiers = [] # OS X api doesn't care it if is left or right
    if (flags & NSControlKeyMask):
        modifiers.append('CONTROL')
    if (flags & NSAlternateKeyMask):
        modifiers.append('ALTERNATE')
    if (flags & NSCommandKeyMask):
        modifiers.append('COMMAND')
    NSLog(u"%@", modifiers)


def initEventMonitor():
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
                                                           | NSFlagsChangedMask,
                                                           handler)


def OnUnexpectedExit(event):
    #
    # Event handler that deals with the unexpected close event.
    #
    #        self.Exit()
    wx.GetApp().ExitMainLoop()


def main():
    app = wx.App(redirect=False)

    app.Bind(wx.EVT_QUERY_END_SESSION, OnUnexpectedExit)
    app.Bind(wx.EVT_END_SESSION, OnUnexpectedExit)

    frame = MainFrame(None)
    frame.Show(True)

    initEventMonitor()
    app.MainLoop()

#     app = NSApplication.sharedApplication()
#     delegate = AppDelegate.alloc().init()
#     NSApp().setDelegate_(delegate)
#     AppHelper.runEventLoop()

if __name__ == '__main__':
    main()
