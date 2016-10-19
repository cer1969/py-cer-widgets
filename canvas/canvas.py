# CRISTIAN ECHEVERRÍA RABÍ


import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Canvas']

#-----------------------------------------------------------------------------------------

class Canvas(wx.Window):
    "Window with double buffer"

    def __init__(self, parent, id=-1, pos=(-1,-1), size=(-1,-1), style=wx.SUNKEN_BORDER):
        wx.Window.__init__(self, parent, id, pos, size, style)
        self.Bind(wx.EVT_PAINT, self._onPaint)
        self.Bind(wx.EVT_SIZE, self._onSize)
        #self.SetDoubleBuffered(True)
        #print ">>>>", self.IsDoubleBuffered()
        self._onSize()
    
    def _onPaint(self, event):
        _dc = wx.BufferedPaintDC(self, self.buffer)
    
    def _onSize(self, event=None):
        size  = self.ClientSize
        self.buffer = wx.Bitmap(*size)
        self.UpdateDrawing()
    
    def UpdateDrawing(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #dc = wx.MemoryDC()
        #dc.SelectObject(self.buffer)
        self.Draw(dc)
        self.Refresh()
    
    def SaveFile(self, filename, filetype=wx.BITMAP_TYPE_PNG):
        self.buffer.SaveFile(filename, filetype)
    
    def Draw(self, dc):
        raise NotImplementedError
