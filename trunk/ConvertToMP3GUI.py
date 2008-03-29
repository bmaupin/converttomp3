#!/usr/bin/python
import wx
from wxConvertToMP3GUI import *


class ConvertGUIStatusFrame(ConvertFrame):
    def __init__(self, *args, **kwds):
        ConvertFrame.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_BUTTON, self.onExitButton, self.exitButton)

    def onClose(self, event):
        self.GetParent().Close()
    
    def onExitButton(self, event):
        self.Close()

class ConvertGUIMainFrame(MainFrame):
    def __init__(self, *args, **kwds):
        MainFrame.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_BUTTON, self.onBeginConvert, self.beginConvert)
        self.Bind(wx.EVT_BUTTON, self.onToConvertBrowse, self.toConvertBrowse)
        self.Bind(wx.EVT_TEXT, self.onToConvertText, self.toConvert)

    def onToConvertBrowse(self, event):
        dd = wx.DirDialog(None, style=wx.DD_DIR_MUST_EXIST)
        if dd.ShowModal() == wx.ID_OK:
            self.toConvert.SetValue(dd.GetPath())
            #evt = wx.CommandEvent(wx.wxEVT_COMMAND_TEXT_UPDATED, self.toConvert.GetId())
            #self.toConvert.AddPendingEvent(evt) # Text update doesn't always seem to be called after browsing

    def onToConvertText(self, event):
        if self.toConvert.GetValue() != "":
            self.status.SetForegroundColour(wx.Colour(0,255,0))
            self.destination.Enable()
            self.destinationBrowse.Enable()
            self.beginConvert.Enable()
            self.status.SetLabel("Ready to begin conversion")
            src = self.toConvert.GetValue()
            if src[-1] == "/":
                src = src[:-1]
            self.destination.SetValue(src + "_mp3")
        else:
            self.status.SetForegroundColour(wx.Colour(255,0,0))
            self.destination.Enable(False)
            self.destinationBrowse.Enable(False)
            self.beginConvert.Enable(False)
            self.status.SetLabel("Please select a directory containing music files")
            self.destination.SetValue("")

    def onBeginConvert(self, event):
        self.Hide()
        statusFrame = ConvertGUIStatusFrame(self, -1, "")
        statusFrame.SetSize(self.GetSize())
        statusFrame.SetPosition(self.GetPosition())
        statusFrame.Show()


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    ConvertToMP3 = ConvertGUIMainFrame(None, -1, "")
    app.SetTopWindow(ConvertToMP3)
    ConvertToMP3.Show()
    app.MainLoop()