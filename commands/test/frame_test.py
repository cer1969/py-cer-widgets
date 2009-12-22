# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ  

import wx
#from cer.widgets.resource.rxwx import resman
#from cer.widgets.resource.rxjava import resman
from cer.widgets.resource.rxnuvola import resman
from command_test import cmd, mbd, tbd, tbd2

#-----------------------------------------------------------------------------------------

CHEVE_ESTILO = wx.DEFAULT_FRAME_STYLE|wx.CLIP_CHILDREN

class MainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"Parábola",size=(700,550),style=CHEVE_ESTILO)

        self.SetMenuBar(mbd.Make())
        self.SetToolBar(tbd.Make(self))
        self.CreateStatusBar(2)
        #self.SetIcon(wx.Icon("Tao.ico",wx.BITMAP_TYPE_ICO))     # Icono de archivo
        appres = wx.GetApp().resman
        #self.SetIcon(appres.Icon("cw_new"))                     # Icono de recurso
        #fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(".xls")
        #print fileType.GetIconInfo()
        #self.SetIcon(fileType.GetIcon())                         # Icono de extensión de sistema

        box = wx.BoxSizer(wx.HORIZONTAL)

        split = wx.SplitterWindow(self,-1,style=wx.SP_3D)
        split.SetBackgroundColour("gray")
        p1 = wx.Panel(split,-1,style=wx.SUNKEN_BORDER)
        p2 = wx.Panel(split,-1,style=wx.SUNKEN_BORDER)
        split.SplitHorizontally(p1,p2,200)
        split.SetMinimumPaneSize(50)
        box.Add(split,1,wx.EXPAND|wx.ALL,0)

        self.tb2 = tbd2.Make(self)
        box.Add(self.tb2,0,wx.EXPAND|wx.ALL|wx.FIXED_MINSIZE ,0)

        self.SetAutoLayout(True)
        self.SetSizer(box)

        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        cmd.Bind(self)
        self.Center(wx.BOTH)

    def OnCloseWindow(self,event=None):
        self.Destroy()

    def Test(self,event=None):
        idx = event.GetId()
        print idx
        #tb = self.GetToolBar()
        #print tb.GetToolState(idx)
        #if tbd.ArgsDict.has_key(idx):
        #    print "Tool idx=",tbd.ArgsDict[idx]

        #mb = self.GetMenuBar()
        #sm = mb.GetMenu(1).GetMenuItems()[0].GetSubMenu()
        #id_metodo_wx = sm.GetMenuItems()[0].GetId()
        #print id_metodo_wx

    def HideTool2(self,event):
        box = self.GetSizer()
        box.Show(self.tb2,False)
        box.Layout()

    def ShowTool2(self,event):
        box = self.GetSizer()
        box.Show(self.tb2,True)
        box.Layout()
        
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    #from wx.lib import colourdb
    #print wx.PlatformInfo
    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.resman = resman
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    #colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
