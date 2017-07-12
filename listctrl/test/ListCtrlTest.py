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
h2 = [lc.Number("Hola"), lc.Number("Chao"), lc.Number("Ok")]


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
        self.lista1 = lc.ListCtrl(p, h1, size=(500,150))
        #self.lista1.attrs[1] = wx.ListItemAttr(wx.NullColor, "LIGHT YELLOW")
        self.lista1.attrs[1] = wx.ListItemAttr()
        self.lista1.attrs[1].SetBackgroundColour("LIGHT YELLOW")
        self.lista1.data = MyData()
        self.lista1.selection = 3
        self.lista1.Bind(wx.EVT_LEFT_DCLICK, self.onDClick1)
        box1.Add(self.lista1, 1, wx.EXPAND|wx.ALL)
        box.Add(box1, 1, wx.EXPAND|wx.ALL, 5)
        
        box2 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "RowDataModel"), wx.VERTICAL)
        self.lista2 = lc.ListCtrl(p, h2, size=(500,150))
        self.lista2.attrs[1] = wx.ListItemAttr()
        self.lista2.attrs[1].SetBackgroundColour("LIGHT BLUE")

        self.lista2.data = lc.RowData(dat2)
        self.lista2.Bind(wx.EVT_LEFT_DCLICK, self.onDClick2)
        box2.Add(self.lista2, 1, wx.EXPAND|wx.ALL)
        box.Add(box2, 1, wx.EXPAND|wx.ALL, 5)
        
        box3 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "ObjDataModel"), wx.VERTICAL)
        self.lista3 = lc.ListCtrl(p, h3, size=(500,150))
        self.lista3.data = lc.ObjData(dat3)
        self.lista3.selection = 3
        self.lista3.Bind(wx.EVT_LEFT_DCLICK, self.onDClick3)
        box3.Add(self.lista3, 1, wx.EXPAND|wx.ALL)
        box.Add(box3, 1, wx.EXPAND|wx.ALL, 5)
        
        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)
        
        self.Fit()
        
        self.lista1.headers[0].text = u"Argentina"
        
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Center(wx.BOTH)

    def onCloseWindow(self, event):
        self.Destroy()
    
    def onDClick1(self, event):
        print(self.lista1.OnGetItemText(self.lista1.selection, 0))
        print(self.lista1.selectedItem)
        headers = self.lista1.headers
        headers[0].text = u"Chile"
        headers[1].width = 100
        headers[1].align = wx.LIST_FORMAT_CENTER
        self.lista1.UpdateView()
    
    def onDClick2(self, event):
        print(self.lista2.selectedItem)
        self.lista1.headers[0].text = u"Otro"
        self.lista1.UpdateView()
    
    def onDClick3(self, event):
        item = self.lista3.selectedItem
        print(item.values())
        print(item.d)

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.App(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.APP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
