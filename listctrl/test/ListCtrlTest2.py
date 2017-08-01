# CRISTIAN ECHEVERRÍA RABÍ 

import sys
from datetime import datetime
import wx
import wx.dataview as dv
#import cer.widgets.listctrl as lc

#----------------------------------------------------------------------

def cmp(a, b): return (a > b) - (a < b)

#-----------------------------------------------------------------------------------------

# Simple Virtual Model
class MyData1(dv.DataViewVirtualListModel):
    def __init__(self):
        dv.DataViewVirtualListModel.__init__(self, 30)
    def GetColumnType(self, col):
        return "string"
    def GetValueByRow(self, row, col):
        return "Row %d, Col %d" % (row, col)
    def GetColumnCount(self):
        return 4
    def GetCount(self):
        return 30
    def GetAttrByRow(self, row, col, attr):
        flag = False
        if (row % 2) == 1:
            attr.SetBackgroundColour("lightyellow")
            flag = True
        if col == 1:
            attr.SetColour('blue')
            attr.SetBold(True)
            flag = True
        return flag

# List Data Model
class MyData2(dv.DataViewIndexListModel):
    def __init__(self):
        dv.DataViewIndexListModel.__init__(self, 21)
        data = [[x,2,3] for x in range(20)]
        data.append([None,4,5])
        self.data = data
    def GetColumnType(self, col):
        return "int"
    def GetValueByRow(self, row, col):
        val = self.data[row][col]
        if val is None:
            return ""
        else:
            return val
    def GetColumnCount(self):
        return len(self.data[0])
    def GetCount(self):
        return len(self.data)
    def GetAttrByRow(self, row, col, attr):
        flag = False
        if (row % 2) == 1:
            attr.SetBackgroundColour("lightblue")
            flag = True
        return flag
    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        v1 = self.data[row1][col]
        v2 = self.data[row2][col]
        v1 = -1 if v1 is None else v1
        v2 = -1 if v2 is None else v2
        return cmp(v1, v2)

# Object Data Model
class dato(object):
    b = "A"
    c = 2.5
    def __init__(self, a):
        self.a = a
        self.d = datetime.now()
    def values(self):
        return (self.a, self.b, self.c, self.d)

types_info = {
    "int":   ("%d",   -sys.maxsize),
    "text":  (None,   ""),
    "float": ("%.2f", -sys.maxsize),
    "date":  (None,   datetime(1,1,1))
}

class MyData3(dv.DataViewIndexListModel):
    def __init__(self):
        dv.DataViewIndexListModel.__init__(self, 11)
        data = [dato(x) for x in range(10)]
        u = dato(100)
        u.d = None
        data.append(u)
        self.data = data
    def GetColumnType(self, col):
        return ["int", "text", "float", "date"][col]
    def GetValueByRow(self, row, col):
        d = self.data[row]
        value = (d.a, d.b, d.c, d.d)[col]
        info = types_info[self.GetColumnType(col)]
        if value is None:
            return info[1]
        else:
            if info[0] is None:
                return value
            else:
                return info[0] % value
    def GetColumnCount(self):
        return 4
    def GetCount(self):
        return len(self.data)
    def GetAttrByRow(self, row, col, attr):
        flag = False
        if (row % 2) == 1:
            attr.SetBackgroundColour("lightgreen")
            flag = True
        return flag
    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.data[self.GetRow(item1)]
        row2 = self.data[self.GetRow(item2)]
        v1 = (row1.a, row1.b, row1.c, row1.d)[col]
        v2 = (row2.a, row2.b, row2.c, row2.d)[col]
        info = types_info[self.GetColumnType(col)]
        v1 = info[1] if v1 is None else v1
        v2 = info[1] if v2 is None else v2
        return cmp(v1, v2)

#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "New ListCtrl Test")
        
        p = wx.Panel(self,-1)
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        box1 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "MyData"), wx.VERTICAL)

        self.lista1 = dv.DataViewCtrl(p, size=(500, 150),
                                      style=wx.BORDER_THEME
                                      #| dv.DV_ROW_LINES # nice alternating bg colors
                                      | dv.DV_HORIZ_RULES
                                      | dv.DV_VERT_RULES
                                      #| dv.DV_MULTIPLE
                                      )
        self.model1 = MyData1()
        self.lista1.AssociateModel(self.model1)
        self.lista1.AppendTextColumn("A", 0, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista1.AppendTextColumn("B", 1, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista1.AppendTextColumn("C", 2, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista1.AppendTextColumn("D", 3, width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista1.Select(self.model1.GetItem(3))
        self.lista1.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.onDClick1)
        box1.Add(self.lista1, 1, wx.EXPAND)
        box.Add(box1, 1, wx.EXPAND|wx.ALL, 5)
        
        box2 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "RowDataModel"), wx.VERTICAL)

        self.lista2 = dv.DataViewCtrl(p, size=(500, 150),
                                      style=wx.BORDER_THEME
                                      | dv.DV_HORIZ_RULES
                                      | dv.DV_VERT_RULES
                                      )
        self.model2 = MyData2()
        self.lista2.AssociateModel(self.model2)
        self.lista2.AppendTextColumn("HOLA", 0, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista2.AppendTextColumn("CHAO", 1, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista2.AppendTextColumn("OK",   2, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        for c in self.lista2.Columns:
            c.Sortable = True
            c.Reorderable = True
        self.lista2.Select(self.model2.GetItem(0))
        self.lista2.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.onDClick2)
        box2.Add(self.lista2, 1, wx.EXPAND|wx.ALL)
        box.Add(box2, 1, wx.EXPAND|wx.ALL, 5)
        
        box3 = wx.StaticBoxSizer(wx.StaticBox(p, -1, "ObjDataModel"), wx.VERTICAL)

        self.lista3 = dv.DataViewCtrl(p, size=(500, 150),
                                      style=wx.BORDER_THEME
                                      | dv.DV_HORIZ_RULES
                                      | dv.DV_VERT_RULES
                                      )
        self.model3 = MyData3()
        self.lista3.AssociateModel(self.model3)
        self.lista3.AppendTextColumn("A", 0, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista3.AppendTextColumn("B", 1, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista3.AppendTextColumn("C", 2, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self.lista3.AppendDateColumn("D", 3, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        for c in self.lista3.Columns:
            c.Sortable = True
            c.Reorderable = True
        self.lista3.Select(self.model3.GetItem(1))
        self.lista3.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.onDClick3)
        box3.Add(self.lista3, 1, wx.EXPAND|wx.ALL)
        box.Add(box3, 1, wx.EXPAND|wx.ALL, 5)
        
        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)
        
        self.Fit()
        
        #self.lista1.headers[0].text = u"Argentina"
        
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Center(wx.BOTH)

    def onCloseWindow(self, event):
        self.Destroy()
    
    def onDClick1(self, event):
        item = self.lista1.GetSelection()
        row = self.model1.GetRow(item)
        print(row)
        self.lista1.Columns[0].Title = "Chile"
    
    def onDClick2(self, event):
        item = self.lista2.GetSelection()
        row = self.model2.GetRow(item)
        print(row)
        self.lista1.Columns[0].Title = "Otro"
    
    def onDClick3(self, event):
        item = self.lista3.GetSelection()
        row = self.model3.GetRow(item)
        print(self.model3.data[row].d)

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.App(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.APP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()
