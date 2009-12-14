# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Canvas']

#-----------------------------------------------------------------------------------------

class Canvas(wx.Window):
    "Window with double buffer"

    def __init__(self, parent, id=-1, pos=(-1,-1), size=(-1,-1), style=wx.SUNKEN_BORDER):
        wx.Window.__init__(self, parent, id, pos, size, style)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.OnSize()
    
    def OnPaint(self, event):
        _dc = wx.BufferedPaintDC(self, self.buffer)
    
    def OnSize(self, event=None):
        size  = self.GetClientSizeTuple()
        self.buffer = wx.EmptyBitmap(*size)
        self.UpdateDrawing()
    
    def UpdateDrawing(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.Draw(dc)
        self.Refresh()
    
    def SaveFile(self, filename, filetype=wx.BITMAP_TYPE_PNG):
        self.buffer.SaveFile(filename, filetype)
    
    def Draw(self, dc):
        raise NotImplementedError
