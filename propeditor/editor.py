# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx
import wx.gizmos as gizmos

#-----------------------------------------------------------------------------------------

__all__ = ['Editor', 'EVTC_PREDIT_VALCHANGE', 'PREDIT_DEF_STYLE']

#-----------------------------------------------------------------------------------------

class _NodeData(object):
    __slots__ = ("Item", "Edit")
    
    def __init__(self, i):
        self.Item = i
        self.Edit = i.Edit

#-----------------------------------------------------------------------------------------

myEVTC_PREDIT_VALCHANGE = wx.NewEventType()
EVTC_PREDIT_VALCHANGE = wx.PyEventBinder(myEVTC_PREDIT_VALCHANGE, 1)

class myEvent(wx.PyCommandEvent):
    def __init__(self, id_, ctrl, item):
        wx.PyCommandEvent.__init__(self, myEVTC_PREDIT_VALCHANGE, id_)
        self.Id = id_
        self.Ctrl = ctrl
        self.Item = item

#-----------------------------------------------------------------------------------------

PREDIT_DEF_STYLE = (wx.TR_DEFAULT_STYLE | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT|
                    wx.TR_HIDE_ROOT | wx.TR_COLUMN_LINES | wx.TR_ROW_LINES) 

class Editor(gizmos.TreeListCtrl):
    """ Widget to display and edit properties
    
    Public attributtes
    FmtGroup  : Tuple with format information for groups
    FmtItem   : Tuple with format information for normal items
    FmtNoEdit : Tuple with format information for non editable items
                Format is (fore, back, bold).
                UpdateFormats or UpdateView must be called after change.
    
    Read-write property
    Data      : EditorData object
    Obj       : Asociated object to manage properties
    
    Write-only property
    MsgBox    : TipBox widget to write messages
    
    """
    
    def __init__(self, parent, data, obj=None, colswidth=(150, 100, 50),
                 colnames=("Propiedad", "Valor", "Uni"), size=(-1, -1),
                 style=PREDIT_DEF_STYLE):
        """
        data      : EditorData object
        obj       : Object to manage properties
        colswidth : Tuple with columns width
        colsnames : Tuple with columns names
        size      : Widget size
        style     : Default to PREDIT_DEF_STYLE
        """
        
        gizmos.TreeListCtrl.__init__(self, parent, -1, size=size, style=style)
        
        self.FmtGroup  = ("BLACK", "LIGHT BLUE", True)
        self.FmtItem   = ("BLACK", "WHITE", False)
        self.FmtNoEdit = ("ROYALBLUE", "LIGHTYELLOW", False)
        
        self._msgBox = None
        
        self.AddColumn(colnames[0], colswidth[0], wx.ALIGN_LEFT)
        self.AddColumn(colnames[1], colswidth[1], wx.ALIGN_RIGHT)
        self.AddColumn(colnames[2], colswidth[2], wx.ALIGN_CENTER)
        self.SetMainColumn(0)
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnItemSelected)
        
        self.Data = data
        self.Obj  = obj

    #-------------------------------------------------------------------------------------
    # Events
    
    def OnItemActivated(self, event):
        n = event.GetItem()
        self.EditNode(n)
        event.Skip()
    
    def OnItemSelected(self, event):
        if self._msgBox is None:
            return
        
        n = event.GetItem()
        nodeData = self.GetPyData(n)
        if nodeData is None:
            return
        self._updateMsgBox(nodeData.Item)
        event.Skip()
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def GetNode(self, item):
        return self._nodeDict[id(item)]
    
    def SetEdit(self, item, edit):
        node = self.GetNode(item)
        nodeData = self.GetPyData(node)
        if nodeData.Item.IsItem:
            nodeData.Edit = edit
        else:
            for i in nodeData.Item:
                self.SetEdit(i, edit)
        self.UpdateFormats(item)
    
    def Edit(self, item):
        node = self.GetNode(item)
        self.EditNode(node)

    def EditNode(self, node):
        nodeData = self.GetPyData(node)
        item = nodeData.Item
        
        if not item.IsItem:
            return
        if not nodeData.Edit:
            return
        
        cur_value = item.GetValue(self._obj)
        new_value = item.Getter(self, cur_value)
        if new_value is None:
            return
        if new_value == cur_value:
            return
        item.SetValue(self._obj, new_value)
        self.UpdateValues(item, setEvent=True)
        self._updateMsgBox(item)
    
    def UpdateView(self):
        self.UpdateValues()
        self.UpdateFormats()
        
    def UpdateFormats(self, item=None):
        if item is None:
            item = self._data
        
        node = self.GetNode(item)
        
        if item.IsItem:
            nodeAttr = self.GetPyData(node)
            attr = self.FmtItem if nodeAttr.Edit else self.FmtNoEdit
        else:
            attr = self.FmtGroup
            for i in item:
                self.UpdateFormats(i)
        
        fg, bg, bold = attr
        self.SetItemTextColour(node, fg)
        self.SetItemBackgroundColour(node, bg)
        self.SetItemBold(node, bold)
    
    def UpdateValues(self, item=None, setEvent=False):
        if item is None:
            item = self._data
        
        if item.IsItem:
            n = self.GetNode(item)
            self.SetItemText(n, item.GetText(self._obj), 1)
            if setEvent:
                evt = myEvent(self.GetId(), self, item)
                self.GetEventHandler().ProcessEvent(evt)
        else:
            for i in item:
                self.UpdateValues(i, setEvent)
    
    #-------------------------------------------------------------------------------------
    # Private methos

    def _addNode(self, node, group):
        for i in group:
            n = self.AppendItem(node, i.Name)
            self.SetItemText(n, i.Unit, 2)
            self.SetPyData(n, _NodeData(i))
            self._nodeDict[id(i)] = n
            if not i.IsItem:
                self._addNode(n, i)
    
    def _updateMsgBox(self, i): 
        if self._msgBox is None:
            return
        _value = i.GetText(self._obj) if i.IsItem else ""
        self._msgBox.SetText(i.Name, i.Msg, _value)

    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _getData(self):
        return self._data
    
    def _setData(self, value):
        self.DeleteAllItems()
        
        self._data = value
        self._nodeDict = {} # relaciona items in EditorData con nodos
        
        root = self.AddRoot(self._data.Name)
        self._nodeDict[id(self._data)] = root
        
        self._addNode(root, self._data)
        self.UpdateFormats()
        self.ExpandAll(root)
    
    def _getObj(self):
        return self._obj
    
    def _setObj(self, value):
        if value is None:
            self._obj = self._data.CreateObj()
        else:
            self._obj = value
        self.UpdateValues()
        
    def _setMsgBox(self, value):
        self._msgBox = value
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    Data   = property(_getData, _setData)
    Obj    = property(_getObj,  _setObj)
    MsgBox = property(None,     _setMsgBox)