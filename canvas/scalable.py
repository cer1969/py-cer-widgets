# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division

#-----------------------------------------------------------------------------------------

__all__ = ['Scalable']

#-----------------------------------------------------------------------------------------

class Scalable(object):
    """Base class for scalable objects"""
    
    def __init__(self, sx=1, sy=1): 
        self.scale = (sx, sy)
    
    def getPoint(self, x, y):
        sx, sy = self.scale
        return (sx*x, sy*y)
    
    def getSize(self, w, h):
        pw, ph = self.getPoint(w, h)
        return (abs(pw), abs(ph))
    
    def getRadius(self, radius):
        #return (pwr**2 + phr**2)**0.5
        return max(self.getSize(radius, radius))
    
    def getRectangle(self, x, y, w, h, radius=0):
        px1, py1 = self.getPoint(x, y)
        px2, py2 = self.getPoint(x + w, y + h) 
        px = min(px1, px2)
        py = min(py1, py2)
        pw, ph = self.getSize(w, h)
        pradius = self.getRadius(radius) 
        return (px, py, pw, ph, pradius)