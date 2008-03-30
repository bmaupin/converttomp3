#!/usr/bin/python
import wx
import os, sys, subprocess, fcntl
from wxConvertToMP3GUI import *


class ConvertGUIStatusFrame(ConvertFrame):
    def __init__(self, *args, **kwds):
        ConvertFrame.__init__(self, *args, **kwds)
        
        self.process = None
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_BUTTON, self.onExitButton, self.exitButton)
        wx.CallLater(1000, self.idleLoop)
        
    def onClose(self, event):
        self.GetParent().Close()
    
    def onExitButton(self, event):
        self.Close()
    
    def beginConversion(self, sourceDir, destDir):
        cmd = [unicode(sys.executable, 'UTF-8'), u'-u', u'ConvertToMP3.py', sourceDir, destDir]
        fse = sys.getfilesystemencoding()
        cmd = [arg.encode(fse) if isinstance(arg,unicode) else arg for arg in cmd]
        self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=os.environ, cwd=os.getcwd())
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    def idleLoop(self):
        if self.process is not None:
            output_stream = self.process.stdout
            try:
                text = output_stream.read()
                self.progress.AppendText(text + '\n')
            except IOError, e:
                if e.errno == 11:
                    pass
                else:
                    raise
            if self.process.poll() != None:
                self.processEnded()
        wx.CallLater(1000, self.idleLoop)

    def processEnded(self):
        self.process = None
        self.status.SetForegroundColour(wx.Colour(0,255,0))
        self.status.SetLabel("Conversion process complete")

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
        statusFrame.beginConversion(self.toConvert.GetValue(), self.destination.GetValue())


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    ConvertToMP3 = ConvertGUIMainFrame(None, -1, "")
    app.SetTopWindow(ConvertToMP3)
    ConvertToMP3.Show()
    app.MainLoop()