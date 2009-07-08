# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import math
from scalable import Scalable

#-----------------------------------------------------------------------------------------

__all__ = ['GraphicsPath']

#-----------------------------------------------------------------------------------------

NOAPLICA  = ()
PENDIENTE = ("AddCurveToPoint", "AddPath", "AddQuadCurveToPoint",
             "CloseSubpath", "Contains", "GetBox", "GetCurrentPoint", "Transform",
             "GetNativePath", "UnGetNativePath")


class GraphicsPath(Scalable):
    """Proxy class for wx.GraphicsPath"""
    
    def __init__(self, gp, scale):
        Scalable.__init__(self, *scale)
        self.gp = gp
    
    def __getattr__(self, name):
        if name in NOAPLICA:
            raise AttributeError("%s not valid for %s" % (name, self.__class__))
        if name in PENDIENTE:
            raise NotImplementedError("%s not implemented for %s" % (name, self.__class__))
        return getattr(self.gc, name)
    
    def MoveToPoint(self, x, y):
        self.gp.MoveToPoint(*self.getPoint(x, y))
    
    def AddLineToPoint(self, x, y):
        return self.gp.AddLineToPoint(*self.getPoint(x, y))
    
    def AddEllipse(self, x, y, w, h):
        return self.gp.AddEllipse(*self.getRectangle(x, y, w, h)[:4])
    
    def AddRectangle(self, x, y, w, h):
        return self.gp.AddRectangle(*self.getRectangle(x, y, w, h)[:4])
    
    def AddRoundedRectangle(self, x, y, w, h, radius):
        return self.gp.AddRoundedRectangle(*self.getRectangle(x, y, w, h, radius))
    
    def AddArc(self, x, y, radius, startAngle, endAngle, clockwise=True):
        px, py = self.getPoint(x, y)
        pradius = self.getRadius(radius)
        ang1 = math.radians(startAngle)
        ang2 = math.radians(endAngle)
        self.gp.AddArc(px, py, pradius, ang1, ang2, clockwise)
    
    def AddArcToPoint(self, x1, y1, x2, y2, radius):
        px1, py1 = self.getPoint(x1, y1)
        px2, py2 = self.getPoint(x2, y2)
        pradius = self.getRadius(radius)
        print "Path.AddArcToPoint: Requiere revisión"
        self.gp.AddArcToPoint(px1, py1, px2, py2, pradius)
    
    def AddCircle(self, x, y, radius):
        px, py = self.getPoint(x, y)
        pradius = self.getRadius(radius)
        self.gp.AddCircle(px, py, pradius)