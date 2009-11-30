# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import math

#-----------------------------------------------------------------------------------------

__all__ = ['AffineMatrix']

#-----------------------------------------------------------------------------------------

class AffineMatrix(object):
    """Represents affine matrix"""
    
    def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
        self.SetMatrix(a, b, c, d, tx, ty)
        self.states = []

    #-------------------------------------------------------------------------------------

    def SetMatrix(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.tx = tx
        self.ty = ty
    
    def SetMatrixFromPoints(self, up1, pp1, up2, pp2):
        """ up1 : User point 1
            pp1 : Pixel point 1 related with up1
            up2 : User point 2
            pp2 : Pixel point 2 related with up2
        """
        self.a = (pp2[0] - pp1[0])/(up2[0] - up1[0])
        self.b = 0
        self.c = 0
        self.d = (pp2[1] - pp1[1])/(up2[1] - up1[1])
        self.tx = pp1[0] - self.a*up1[0]
        self.ty = pp1[1] - self.d*up1[1]
    
    def SetMatrixFromFrame(self, up1, up2, psize, margins=(0, 0, 0, 0)):
        """ up1     : User point 1 (bottom-left corner)
            up2     : User point 2 (top-right corner)
            psize   : Frame size in pixels
            margins : Frame margins in pixels (left, rigth, top, bottom)
        """
        self.a = (psize[0] - margins[0] - margins[1])/(up2[0] - up1[0])
        self.b = 0
        self.c = 0
        self.d = (psize[1] - margins[2] - margins[3])/(up1[1] - up2[1])
        self.tx = margins[0] - self.a*up1[0]
        self.ty = margins[2] - self.d*up2[1]
    
    #-------------------------------------------------------------------------------------
    # Private methods
    
    def getPoint(self, x, y):
        px = self.a*x + self.b*y + self.tx
        py = self.c*x + self.d*y + self.ty
        return (px, py)
    
    def getPoints(self, points):
        return [self.getPoint(*p) for p in points]
    
    def getSize(self, w, h):
        px0, py0 = self.getPoint(0, 0)
        # cálculo de pw
        pxw, pyw = self.getPoint(w, 0)
        pw = ((pxw - px0)**2 + (pyw - py0)**2)**0.5
        # cálculo de ph
        pxh, pyh = self.getPoint(0, h)
        ph = ((pxh - px0)**2 + (pyh - py0)**2)**0.5
        return (pw, ph)
    
    def getRadius(self, radius):
        #return (pwr**2 + phr**2)**0.5
        return max(self.getSize(radius, radius))

    def getRectanglePoints(self, x, y, w, h):
        p1 = self.getPoint(x, y)
        p2 = self.getPoint(x, y+h)
        p3 = self.getPoint(x+w, y+h)
        p4 = self.getPoint(x+w, y) 
        return (p1, p2, p3, p4)
    
    def getEllipsePoints(self, x, y, w, h, np=30):
        xo = x + w/2
        yo = y + h/2
        sal = []
        for i in range(np):
            angle = math.radians(360*i/np)
            xk = (w/2)*math.cos(angle) + xo
            yk = (h/2)*math.sin(angle) + yo
            sal.append((xk, yk))
        return [self.getPoint(*p) for p in sal]
    
    def getCirclePoints(self, x, y, radius, np=30):
        sal = []
        for i in range(np):
            angle = math.radians(360*i/np)
            xk = radius*math.cos(angle) + x
            yk = radius*math.sin(angle) + y
            sal.append((xk, yk))
        return [self.getPoint(*p) for p in sal]
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def Translate(self, dx, dy):
        px0, py0 = self.getPoint(0, 0)
        px1, py1 = self.getPoint(dx, dy)
        self.tx = self.tx + (px1 - px0)
        self.ty = self.ty + (py1 - py0)
    
    def Rotate(self, angle=0):
        angle = math.radians(-angle) # para hacer anticlockwise
        a, b, c, d = self.a, self.b, self.c, self.d
        self.a =  a*math.cos(angle) + b*math.sin(angle)
        self.b = -a*math.sin(angle) + b*math.cos(angle)
        self.c =  c*math.cos(angle) + d*math.sin(angle)
        self.d = -c*math.sin(angle) + d*math.cos(angle)
    
    def Scale(self, sx, sy):
        self.a = sx*self.a
        self.b = sy*self.b
        self.c = sx*self.b
        self.d = sy*self.d
    
    def GetInverse(self):
        # Calculate and return the inverse affine matrix
        a, b, c, d, tx, ty = self.a, self.b, self.c, self.d, self.tx, self.ty
        ai =  d/(a*d - b*c)
        bi = -b/(a*d - b*c)
        ci = -c/(a*d - b*c)
        di =  a/(a*d - b*c)
        txi = (ty*b - tx*d)/(a*d - b*c)
        tyi = (tx*c - ty*a)/(a*d - b*c)
        return AffineMatrix(ai, bi, ci, di, txi, tyi)

    #-------------------------------------------------------------------------------------
    # State method (stack with states)
    
    def PushState(self):
        self.states.append((self.a, self.b, self.c, self.d, self.tx, self.ty))
    
    def PopState(self):
        self.a, self.b, self.c, self.d, self.tx, self.ty = self.states.pop()