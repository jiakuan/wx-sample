#!/usr/bin/env python
  
import icons
import os
import wx
# chose an implementation, depending on os
if os.name == 'nt':  # sys.platform == 'win32':
    import pyHook

if os.name == 'nt':
    def OnMouseEvent(event):
        # called when mouse events are received
        print 'MessageName:', event.MessageName
        print 'Message:', event.Message
        print 'Time:', event.Time
        print 'Window:', event.Window
        print 'WindowName:', event.WindowName
        print 'Position:', event.Position
        print 'Wheel:', event.Wheel
        print 'Injected:', event.Injected
        print '---'
        
        # return True to pass the event to other handlers
        return True

class DemoTaskBarIcon(wx.TaskBarIcon):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE = wx.NewId()
    TBMENU_CHANGE = wx.NewId()
    TBMENU_REMOVE = wx.NewId()
 
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
 
        # Set the image
        icon = self.MakeIcon(icons.wisetime.GetImage())
        self.SetIcon(icon, "wxPython Demo")
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
        menu.Append(self.TBMENU_RESTORE, "Restore wxPython Demo")
        menu.Append(self.TBMENU_CLOSE, "Close wxPython Demo")
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


if __name__ == '__main__':
    print os.name
    if os.name == 'nt':  # sys.platform == 'win32':
        # create a hook manager
        hm = pyHook.HookManager()
        # watch for all mouse events
        hm.MouseAll = OnMouseEvent
        # set the hook
        hm.HookMouse()

    app = wx.App(redirect=False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
