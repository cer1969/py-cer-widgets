# CRISTIAN ECHEVERRÍA RABÍ


import math
import wx

from .scalable import Scalable
from .graphicspath import GraphicsPath

#-----------------------------------------------------------------------------------------

__all__ = ['GraphicsContext']

#-----------------------------------------------------------------------------------------

NOAPLICA  = ("Create", "CreateFromNative", "CreateFromNativeWindow", "CreateMatrix")
PENDIENTE = ("GetTransform", "SetTransform", "ConcatTransform")


class GraphicsContext(Scalable):
    """Proxy class for wx.GraphicsContext"""
    
    def __init__(self, dc):
        Scalable.__init__(self) 
        self.gc = wx.GraphicsContext.Create(dc)
        self.states = []
    
    def __getattr__(self, name):
        if name in NOAPLICA:
            raise AttributeError("%s not valid for %s" % (name, self.__class__))
        if name in PENDIENTE:
            raise NotImplementedError("%s not implemented for %s" % (name, self.__class__))
        return getattr(self.gc, name)
    
    #-------------------------------------------------------------------------------------
    # New public methods
    
    def SetMatrix(self, sx=1, sy=1, tx=0, ty=0):
        self.scale = (sx, sy)
        mx = self.gc.CreateMatrix(1, 0, 0, 1, tx, ty)
        self.gc.SetTransform(mx)
    
    def SetMatrixFromPoints(self, up1, pp1, up2, pp2):
        """ up1 : User point 1
            pp1 : Pixel point 1 related with up1
            up2 : User point 2
            pp2 : Pixel point 2 related with up2
        """
        sx = (pp2[0] - pp1[0])/(up2[0] - up1[0])
        sy = (pp2[1] - pp1[1])/(up2[1] - up1[1])
        tx = pp1[0] - sx*up1[0]
        ty = pp1[1] - sy*up1[1]
        self.SetMatrix(sx, sy, tx, ty)
    
    def SetMatrixFromFrame(self, up1, up2, psize, margins=(0, 0, 0, 0)):
        """ up1     : User point 1 (bottom-left corner)
            up2     : User point 2 (top-right corner)
            psize   : Frame size in pixels
            margins : Frame margins in pixels (left, rigth, top, bottom)
        """
        sx = (psize[0] - margins[0] - margins[1])/(up2[0] - up1[0])
        sy = (psize[1] - margins[2] - margins[3])/(up1[1] - up2[1])
        tx = margins[0] - sx*up1[0]
        ty = margins[2] - sy*up2[1]
        self.SetMatrix(sx, sy, tx, ty)
    
    def DrawAncText(self, str, x, y, angle=0, anchor=wx.RIGHT, pxgap=0, pygap=0,
                    brush=wx.NullGraphicsBrush):
        """Draw text anchored (New from wx.GraphicContext API)
        (ux, uy) : Position to vertically center the text
        angle    : Angle in hexadecimal anticlockwise
        anchor   : Part of the test that anchors to the point (ux, uy)
                   (wx.LEFT, wx.RIGHT, wx.TOP, wx.BOTTOM)
        pxgap    : Distance in x pixels from the anchor border
        pygap    : Distance in y pixels from the anchor border
        brush    : Background brush
        """
        px, py = self.getPoint(x, y) 
        pw, ph = self.gc.GetTextExtent(str)
        
        angle = math.radians(angle)
        
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
        
        self.gc.DrawText(str, px, py, angle, brush)
    
    #-------------------------------------------------------------------------------------
    # Overwritted methods

    def CreateRadialGradientBrush(self, xo, yo, xc, yc, radius, brush1, brush2):
        pxo, pyo = self.getPoint(xo, yo)
        pxc, pyc = self.getPoint(xc, yc)
        pradius = self.getRadius(radius) 
        return self.gc.CreateRadialGradientBrush(pxo, pyo, pxc, pyc, pradius, brush1, brush2)
    
    def CreateLinearGradientBrush(self, x1, y1, x2, y2, brush1, brush2):
        px1, py1 = self.getPoint(x1, y1)
        px2, py2 = self.getPoint(x2, y2)
        return self.gc.CreateLinearGradientBrush(px1, py1, px2, py2, brush1, brush2)
    
    def Clip(self, x1, y1, x2, y2):
        px1, py1 = self.getPoint(x1, y1)
        px2, py2 = self.getPoint(x2, y2)
        print(self.gc.Clip(px1, py1, px2, py2))
    
    def DrawBitmap(self, bitmap, x, y, w, h):
        self.gc.DrawBitmap(bitmap, *self.getRectangle(x, y, w, h)[:4])
    
    def DrawIcon(self, icon, x, y, w, h):
        self.gc.DrawIcon(icon, *self.getRectangle(x, y, w, h)[:4])
    
    def DrawEllipse(self, x, y, w, h):
        self.gc.DrawEllipse(*self.getRectangle(x, y, w, h)[:4])
    
    def DrawRectangle(self, x, y, w, h):
        self.gc.DrawRectangle(*self.getRectangle(x, y, w, h)[:4])
    
    def DrawRoundedRectangle(self, x, y, w, h, radius):
        self.gc.DrawRoundedRectangle(*self.getRectangle(x, y, w, h, radius))
    
    def DrawText(self, str, x, y, angle=0, brush=wx.NullGraphicsBrush):
        """Draw Text (Modified from wx.GraphicContext API)
        (ux, uy) : Top-left position
        angle    : Angle in hexadecimal anticlockwise
        brush    : Background brush
        """
        px, py = self.getPoint(x, y) 
        #self.gc.DrawRotatedText(str, px, py, math.radians(angle), brush)
        self.gc.DrawText(str, px, py, math.radians(angle), brush)
    
    def PushState(self):
        self.gc.PushState()
        self.states.append(self.scale)
    
    def PopState(self):
        self.gc.PopState()
        self.scale = self.states.pop()
    
    def Rotate(self, angle):
        self.gc.Rotate(math.radians(angle))
    
    def Scale(self, usx, usy):
        sx, sy = self.scale
        self.scale = (sx*usx, sy*usy)
    
    def Translate(self, dx, dy):
        px0, py0 = self.getPoint(0, 0)
        px1, py1 = self.getPoint(dx, dy)
        self.gc.Translate((px1 - px0), (py1 - py0))
    
    def StrokeLine(self, x1, y1, x2, y2):
        px1, py1 = self.getPoint(x1, y1)
        px2, py2 = self.getPoint(x2, y2)
        self.gc.StrokeLine(px1, py1, px2, py2)
    
    def StrokeLines(self, upoints):
        ppoints = [self.getPoint(*up) for up in upoints]
        self.gc.StrokeLines(ppoints)

    def DrawLines(self, upoints, fillStyle=wx.ODDEVEN_RULE):
        ppoints = [self.getPoint(*up) for up in upoints]
        self.gc.DrawLines(ppoints, fillStyle)
    
    #-------------------------------------------------------------------------------------
    
    def CreatePath(self):
        return GraphicsPath(self.gc.CreatePath(), self.scale)

    def DrawPath(self, path, fillStyle=wx.ODDEVEN_RULE):
        self.gc.DrawPath(path.gp, fillStyle)

    def FillPath(self, path, fillStyle=wx.ODDEVEN_RULE):
        self.gc.FillPath(path.gp, fillStyle)
        
    def StrokePath(self, path):
        self.gc.StrokePath(path.gp)