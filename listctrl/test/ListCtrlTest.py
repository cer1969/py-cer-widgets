# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import wx
import cer.widgets.listctrl as lc
import datetime

#-----------------------------------------------------------------------------------------

# DataManager
class MyDataManager(lc.DataManager):
    def GetNumberRows(self, data):
        return 25

dm1 = MyDataManager(lc.Text("A"), lc.Text("B"), lc.Text("C"), lc.Text("D"))

# RowDataManager
dm2 = lc.RowDataManager(lc.Text("Hola"), lc.Text("Chao"), lc.Text("Ok"))
dat2 = [(x,2,3) for x in range(20)]
dat2.append((None,4,5))

# ObjDataManager
class dato(object):
    b = "A"
    c = 2.5
    def __init__(self,a):
        self.a = a
        self.d = datetime.datetime.now()
    def values(self):
        return (self.a, self.b, self.c, self.d)

dm3 = lc.ObjDataManager(
    lc.Number("a", format="%d", attr="a"),
    lc.Text("b", attr="b"),
    lc.Number("c", align=wx.LIST_FORMAT_RIGHT, format="%.2f", attr="c"),
    lc.DateTime("d", format="%H:%M:%S", attr="d")
)
u = dato(100)
u.d = None
dat3 = [dato(x) for x in range(10)]
dat3.append(u)

#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,"New ListCtrl Test")

        p = wx.Panel(self,-1)

        box = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "MyDataManager"), wx.VERTICAL)
        self.lc1 = lc.ListCtrl(p, dm1, size=(500,150))
        self.lc1.Attrs[1] = wx.ListItemAttr(wx.NullColor, "LIGHT YELLOW")
        self.lc1.UpdateView()
        self.lc1.Selection = 3
        wx.EVT_LEFT_DCLICK(self.lc1, self.OnDClick1)
        box1.Add(self.lc1, 1, wx.EXPAND|wx.ALL)
        box.Add(box1, 1, wx.EXPAND|wx.ALL, 5)

        box2 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "RowDataManager"), wx.VERTICAL)
        self.lc2 = lc.ListCtrl(p, dm2, size=(500,150))
        self.lc2.Data = dat2
        self.lc2.Attrs[1] = wx.ListItemAttr(wx.NullColor, "LIGHT BLUE")
        self.lc2.UpdateView()
        self.lc2.Selection = 1
        wx.EVT_LEFT_DCLICK(self.lc2, self.OnDClick2)
        box2.Add(self.lc2, 1, wx.EXPAND|wx.ALL)
        box.Add(box2, 1, wx.EXPAND|wx.ALL, 5)
        
        box3 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "ObjDataManager"), wx.VERTICAL)
        self.lc3 = lc.ListCtrl(p, dm3, size=(500,150))
        self.lc3.Data = dat3
        self.lc3.UpdateView()
        self.lc3.Selection = 3
        wx.EVT_LEFT_DCLICK(self.lc3, self.OnDClick3)
        box3.Add(self.lc3, 1, wx.EXPAND|wx.ALL)
        box.Add(box3, 1, wx.EXPAND|wx.ALL, 5)

        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)

        self.Fit()

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Center(wx.BOTH)

    def OnCloseWindow(self,event):
        self.Destroy()

    def OnDClick1(self,event):
        print self.lc1.OnGetItemText(self.lc1.Selection,0)

    def OnDClick2(self,event):
        print self.lc2.OnGetItemText(self.lc2.Selection,0)

    def OnDClick3(self,event):
        print self.lc3.Data[self.lc3.Selection].values()
        #print self.lc3.OnGetItemText(self.lc3.Selection,0)

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
