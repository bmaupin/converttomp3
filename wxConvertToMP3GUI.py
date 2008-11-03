#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Mar 29 13:19:42 2008
#
#    Copyright (C) Brad Smith 2008
#
#    This file is part of ConvertToMP3GUI
#
#    ConvertToMP3GUI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ConvertToMP3GUI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ConvertToMP3GUI.  If not, see <http://www.gnu.org/licenses/>.

import wx

# begin wxGlade: extracode
# end wxGlade



class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.destinationBox_staticbox = wx.StaticBox(self, -1, "Destination Directory for Converted MP3 Files")
        self.toConvertBox_staticbox = wx.StaticBox(self, -1, "Directory to Convert")
        self.toConvert = wx.TextCtrl(self, -1, "")
        self.toConvertBrowse = wx.Button(self, -1, "Browse...")
        self.destination = wx.TextCtrl(self, -1, "")
        self.destinationBrowse = wx.Button(self, -1, "Browse...")
        self.status = wx.StaticText(self, -1, "Please select a directory containing music files")
        self.beginConvert = wx.Button(self, -1, "Begin Converting")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("ConvertToMP3 0.5")
        self.SetSize((800, 400))
        self.destination.Enable(False)
        self.destinationBrowse.Enable(False)
        self.status.SetForegroundColour(wx.Colour(255, 0, 0))
        self.status.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        destinationBox = wx.StaticBoxSizer(self.destinationBox_staticbox, wx.HORIZONTAL)
        toConvertBox = wx.StaticBoxSizer(self.toConvertBox_staticbox, wx.HORIZONTAL)
        toConvertBox.Add(self.toConvert, 1, wx.ALL|wx.EXPAND, 7)
        toConvertBox.Add(self.toConvertBrowse, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 7)
        mainSizer.Add(toConvertBox, 0, wx.ALL|wx.EXPAND, 10)
        destinationBox.Add(self.destination, 1, wx.ALL|wx.EXPAND, 7)
        destinationBox.Add(self.destinationBrowse, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 7)
        mainSizer.Add(destinationBox, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        mainSizer.Add((300, 50), 1, wx.EXPAND, 0)
        statusSizer.Add(self.status, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        statusSizer.Add(self.beginConvert, 0, 0, 0)
        mainSizer.Add(statusSizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(mainSizer)
        self.Layout()
        # end wxGlade

# end of class MainFrame


class ConvertFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ConvertFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.progressBox_staticbox = wx.StaticBox(self, -1, "Conversion Progress")
        self.progress = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.status = wx.StaticText(self, -1, "Conversion in Progress. Please Wait...")
        self.exitButton = wx.Button(self, -1, "Exit")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ConvertFrame.__set_properties
        self.SetTitle("ConvertToMP3 0.5")
        self.status.SetForegroundColour(wx.Colour(255, 0, 0))
        self.status.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ConvertFrame.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        progressBox = wx.StaticBoxSizer(self.progressBox_staticbox, wx.HORIZONTAL)
        progressBox.Add(self.progress, 1, wx.ALL|wx.EXPAND, 7)
        mainSizer.Add(progressBox, 1, wx.ALL|wx.EXPAND, 10)
        statusSizer.Add(self.status, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        statusSizer.Add(self.exitButton, 0, 0, 0)
        mainSizer.Add(statusSizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        # end wxGlade

# end of class ConvertFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    ConvertToMP3 = MainFrame(None, -1, "")
    app.SetTopWindow(ConvertToMP3)
    ConvertToMP3.Show()
    app.MainLoop()
