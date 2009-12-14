# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import wx, time
from cer.widgets import canvas

#-----------------------------------------------------------------------------------------

class MyCanvas(canvas.Canvas):
    
    def Draw(self, dc):
        
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        
        dc = wx.GCDC(dc)
        adc = canvas.AffineDC(dc)
        
        psize = self.GetClientSizeTuple()
        adc.SetMatrixFromFrame((0,0), (10,10), psize, (50,50,50,50))
        #adc.SetMatrixFromFrame((0,psize[1]), (psize[0],0), psize, (0,0,0,0))
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        #font.SetFaceName("Tahoma")
        #font.SetPointSize(9)
        adc.SetFont(font)
        
        #brush = adc.CreateLinearGradientBrush(0, 0, 10, 10,
        #                                      wx.Colour(255, 255, 174, 70),
        #                                      wx.Colour(255, 117, 140, 40))
        
        #brush = mgc.CreateRadialGradientBrush(0, 0, 5, 5, 4,
        #                                      wx.Colour(255, 255, 174, 70),
        #                                      wx.Colour(255, 117, 140, 40))
        
        adc.SetPen(wx.Pen(wx.NamedColour('GRAY50'), 1, wx.SOLID))
        adc.SetBrush(wx.Brush(wx.Colour(255, 255, 219)))
        #adc.Scale(0.8, 1.0)
        adc.Translate(3, 0)
        adc.Rotate(-20)
        adc.DrawRectangle(0, 0, 10, 10)
        
        for i in range(1, 10):
            adc.DrawLine(i, 0, i, 10)
            adc.DrawLine(0, i, 10, i)
            # Valores de y en x = 0 usando anchor wx.RIGHT
            adc.DrawAncText("%d" % i, 0, i, 0, wx.RIGHT, pxgap=-10, pygap=0)
            # Valores de y en x = 10 usando anchor wx.TOP y angle=90°
            adc.DrawAncText("%d" % i, 10, i, 90, wx.TOP, pxgap=10, pygap=0)
            # Valores de x en y = 0 usando anchor wx.TOP (coordenadas cartesianas)
            adc.DrawAncText("%d" % i, i, 0, 0, wx.TOP, pxgap=0, pygap=10)
            # Valores de x en y = 10 usando anchor wx.LEFT y angle=90° (coordenadas cartesianas)
            adc.DrawAncText("%d" % i, i, 10, 90, wx.LEFT, pxgap=0,  pygap=-10)
        
        adc.SetPen(wx.Pen(wx.NamedColour('BLUE'), 2, wx.SOLID))
        adc.SetBrush(wx.Brush(wx.Colour(121, 219, 255)))
        
        adc.DrawLine(0, 0, 1, 1)
        adc.DrawLine(1, 1, 4, 7)
        
        adc.DrawRectangle(6, 6, 2, 2)
        
        adc.PushState()
        adc.SetPen(wx.Pen(wx.NamedColour('RED'), 1, wx.SOLID))
        adc.SetBrush(wx.Brush(wx.Colour(216, 89, 255, 100), wx.CROSSDIAG_HATCH))
        adc.Translate(6, 1)
        adc.DrawCircle(1, 2, 2)
        #adc.DrawEllipse(1, 1, 3, 3)
        adc.DrawEllipse(1, 2, 2, 2)
        adc.PopState()
        
        #adc.SetPen(wx.Pen(wx.NamedColour('BLUE'), 1, wx.SOLID))
        #adc.SetBrush(wx.Brush(wx.Colour(34,  34,  178, 100)))
        
        #bitmap = wx.Bitmap("transelec.png")
        im = wx.Image("transelec.png")
        im.Rescale(im.GetWidth()/4, im.GetHeight()/4, wx.IMAGE_QUALITY_HIGH)
        bitmap = im.ConvertToBitmap()
        adc.DrawBitmap(bitmap, 0.1, 9.1)
        
        adc.DrawEllipse(1, 1, 3, 2)
        adc.DrawEllipse(2, 2, 2, 2)
        adc.DrawEllipse(3, 3, 2, 2)
        
        adc.DrawText("Hola", 2, 2, 90)
        
        #adc.DrawLines([(1,1), (1,8), (8,8)])
        adc.DrawSpline([(1,1), (1,8), (8,8)])
        
        #path = adc.CreatePath()
        #path.MoveToPoint(0, 0)
        #path.AddLineToPoint(0, 1)
        #path.AddLineToPoint(1, 0)
        #path.AddEllipse(0.5, 0.5, 1, 1)
        #path.MoveToPoint(0, 0)
        #path.AddCircle(0, 0, 1)
        #path.AddRoundedRectangle(0, 0, 2, 3, 0.2)
        #path.AddLineToPoint(1, 1)
        
        #adc.Translate(2, 3)
        #adc.DrawPath(path)
        #adc.Translate(5, 5)
        #adc.FillPath(path)

#- <00> -----------------------------------------------------------------------

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Wx-Template")
        
        self.canvas = MyCanvas(self)
        self.CreateStatusBar()
        self.SetClientSizeWH(500, 500)
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.canvas, 0, wx.LEFT|wx.TOP, 0)
        
        self.SetSizer(box)
        self.SetAutoLayout(True)
        
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        #self.OnSize()
        #wx.FutureCall(2000, self.ShowMessage) # se puede pasar args
        
        print "Inicio: %f" % time.clock()

    def OnSize(self, event=None):
        s = min(self.GetClientSizeTuple())
        self.canvas.SetClientSizeWH(s, s)
        print "New size: %s" % s
        
    def ShowMessage(self):
        msg = "Fin: %f" % time.clock()
        wx.MessageBox(msg, 'Mensaje')
        
    def OnCloseWindow(self, event=None):
        print "Maximized: %s" % self.IsMaximized()
        self.Destroy()


#- <99> -----------------------------------------------------------------------

if __name__ == '__main__':
    from wx.lib import colourdb
    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
