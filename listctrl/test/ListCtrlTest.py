# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import wx
import cer.widgets.listctrl as lc
from datetime import datetime

#-----------------------------------------------------------------------------------------

# Personal DataModel
class MyData(lc.BaseData):
    def __len__(self):
        return 30

h1 = [lc.Text("A"), lc.Text("B"), lc.Text("C"), lc.Text("D")]


# RowDataModel
dat2 = [[x,2,3] for x in range(20)]
dat2.append([None,4,5])
h2 = [lc.Text("Hola"), lc.Text("Chao"), lc.Text("Ok")]


# ObjDataModel
class dato(object):
    b = "A"
    c = 2.5
    def __init__(self, a):
        self.a = a
        self.d = datetime.now()
    def values(self):
        return (self.a, self.b, self.c, self.d)

dat3 = [dato(x) for x in range(10)]
u = dato(100)
u.d = None
dat3.append(u)

h3 = [
    lc.Number("a", format="%d", attr="a"),
    lc.Text("b", attr="b"),
    lc.Number("c", align=wx.LIST_FORMAT_RIGHT, format="%.2f", attr="c"),
    lc.DateTime("d", format="%H:%M:%S", attr="d")
]

#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "New ListCtrl Test")
        
        p = wx.Panel(self,-1)
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        box1 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "MyData"), wx.VERTICAL)
        self.lc1 = lc.ListCtrl(p, h1, size=(500,150))
        self.lc1.attrs[1] = wx.ListItemAttr(wx.NullColor, "LIGHT YELLOW")
        self.lc1.data = MyData()
        self.lc1.selection = 3
        wx.EVT_LEFT_DCLICK(self.lc1, self.onDClick1)
        box1.Add(self.lc1, 1, wx.EXPAND|wx.ALL)
        box.Add(box1, 1, wx.EXPAND|wx.ALL, 5)
        
        box2 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "RowDataModel"), wx.VERTICAL)
        self.lc2 = lc.ListCtrl(p, h2, size=(500,150))
        self.lc2.attrs[1] = wx.ListItemAttr(wx.NullColor, "LIGHT BLUE")
        self.lc2.data = lc.RowData(dat2)
        wx.EVT_LEFT_DCLICK(self.lc2, self.onDClick2)
        box2.Add(self.lc2, 1, wx.EXPAND|wx.ALL)
        box.Add(box2, 1, wx.EXPAND|wx.ALL, 5)
        
        box3 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "ObjDataModel"), wx.VERTICAL)
        self.lc3 = lc.ListCtrl(p, h3, size=(500,150))
        self.lc3.data = lc.ObjData(dat3)
        self.lc3.selection = 3
        wx.EVT_LEFT_DCLICK(self.lc3, self.onDClick3)
        box3.Add(self.lc3, 1, wx.EXPAND|wx.ALL)
        box.Add(box3, 1, wx.EXPAND|wx.ALL, 5)
        
        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)
        
        self.Fit()
        
        self.lc1.headers[0].text = u"Argentina"
        
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Center(wx.BOTH)

    def onCloseWindow(self, event):
        self.Destroy()
    
    def onDClick1(self, event):
        print self.lc1.OnGetItemText(self.lc1.selection, 0)
        print self.lc1.selectedItem
        headers = self.lc1.headers
        headers[0].text = u"Chile"
        headers[1].width = 100
        headers[1].align = wx.LIST_FORMAT_CENTER
        self.lc1.updateView()
    
    def onDClick2(self, event):
        print self.lc2.selectedItem
        self.lc1.headers[0].text = u"Otro"
        self.lc1.updateView()
    
    def onDClick3(self, event):
        item = self.lc3.selectedItem
        print item.values()
        print item.d

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
