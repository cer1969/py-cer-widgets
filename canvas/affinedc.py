# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import math
import wx

from affinematrix import AffineMatrix 

#-----------------------------------------------------------------------------------------

__all__ = ['AffineDC']

#-----------------------------------------------------------------------------------------

NOAPLICA  = ()
PENDIENTE = ()


class AffineDC(AffineMatrix):

    def __init__(self, dc):
        AffineMatrix.__init__(self)
        self.dc = dc
    
    def __getattr__(self, name):
        if name in NOAPLICA:
            raise AttributeError("%s not valid for %s" % (name, self.__class__))
        if name in PENDIENTE:
            raise NotImplementedError("%s not implemented for %s" % (name, self.__class__))
        return getattr(self.dc, name)
    
    def DrawPoint(self, x, y):
        px, py = self.getPoint(x, y)
        self.dc.DrawPoint(px, py)
    
    def DrawPointList(self, points, pens=None):
        ppoints = [self.getPoint(*x) for x in points]
        self.dc.DrawPointList(ppoints, pens)
    
    def DrawLine(self, x1, y1, x2, y2):
        px1, py1 = self.getPoint(x1, y1)
        px2, py2 = self.getPoint(x2, y2)
        self.dc.DrawLine(px1, py1, px2, py2)
    
    StrokeLine = DrawLine
    
    def DrawLines(self, points, xoffset=0, yoffset=0):
        ppoints = [self.getPoint(*x) for x in points]
        self.dc.DrawLines(ppoints, xoffset, yoffset)
    
    StrokeLines = DrawLines
    
    def DrawSpline(self, points):
        ppoints = [self.getPoint(*x) for x in points]
        self.dc.DrawSpline(ppoints)
    
    def DrawRectangle(self, *args):
        self.dc.DrawPolygon(self.getRectanglePoints(*args))
    
    def DrawEllipse(self, *args):
        self.dc.DrawPolygon(self.getEllipsePoints(*args))
    
    def DrawCircle(self, *args):
        self.dc.DrawPolygon(self.getCirclePoints(*args))
    
    def DrawBitmap(self, bitmap, x, y, transparent=True):
        px, py = self.getPoint(x, y)
        self.dc.DrawBitmap(bitmap, px, py, transparent)
    
    def DrawText(self, str, x, y, angle=0):
        """Draw Text (Modified from wx.GraphicContext API)
        (ux, uy) : Top-left position
        angle    : Angle in hexadecimal anticlockwise
        """
        px, py = self.getPoint(x, y)
        self.dc.DrawRotatedText(str, px, py, angle)
    
    def DrawAncText(self, str, x, y, angle=0, anchor=wx.RIGHT, pxgap=0, pygap=0):
        """Draw text anchored (New from wx.GraphicContext API)
        (ux, uy) : Position to vertically center the text
        angle    : Angle in hexadecimal anticlockwise
        anchor   : Part of the test that anchors to the point (ux, uy)
                   (wx.LEFT, wx.RIGHT, wx.TOP, wx.BOTTOM)
        pxgap    : Distance in x pixels from the anchor border
        pygap    : Distance in y pixels from the anchor border
        """
        px, py = self.getPoint(x, y) 
        pw, ph = self.dc.GetTextExtent(str)
        
        if anchor == wx.LEFT:
            px = px + pxgap - (ph/2)*math.sin(angle)
            py = py + pygap - (ph/2)*math.cos(angle)
        elif anchor == wx.RIGHT:
            px = px + pxgap - pw*math.cos(angle) - (ph/2)*math.sin(angle)
            py = py + pygap + pw*math.sin(angle) - (ph/2)*math.cos(angle)
        elif anchor == wx.TOP:
            px = px + pxgap - (pw/2)*math.cos(angle)
            py = py + pygap + (pw/2)*math.sin(angle) 
        else:
            px = px + pxgap - (pw/2)*math.cos(angle) - ph*math.sin(angle)
            py = py + pygap + (pw/2)*math.sin(angle) - ph*math.cos(angle)
        
        self.dc.DrawRotatedText(str, px, py, angle)
