# CRISTIAN ECHEVERRÍA RABÍ

import wx
import wx.lib.newevent
#import wx.dataview as dv

#-----------------------------------------------------------------------------------------

__all__ = ['Editor', 'EVTC_PREDIT_VALCHANGE', 'PREDIT_DEF_STYLE']

#-----------------------------------------------------------------------------------------

class _NodeData(object):
    __slots__ = ("Item", "Edit")
    
    def __init__(self, i):
        self.Item = i
        self.Edit = i.Edit

#-----------------------------------------------------------------------------------------

myEvent, EVTC_PREDIT_VALCHANGE = wx.lib.newevent.NewEvent()

#PREDIT_DEF_STYLE = dv.TL_DEFAULT_STYLE # | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT|
#                    #wx.TR_HIDE_ROOT | wx.TR_ROW_LINES) # dataview.TR_COLUMN_LINES
PREDIT_DEF_STYLE = wx.LC_REPORT | wx.LC_VRULES


class Editor(wx.ListCtrl):
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
        
        wx.ListCtrl.__init__(self, parent, -1, size=size, style=style)
        
        self.FmtGroup  = ("BLACK", "LIGHT BLUE", True)
        self.FmtItem   = ("BLACK", "WHITE", False)
        self.FmtNoEdit = ("ROYALBLUE", "LIGHTYELLOW", False)
        
        self._msgBox = None
        
        self.AppendColumn(colnames[0], wx.LIST_FORMAT_LEFT,   colswidth[0])
        self.AppendColumn(colnames[1], wx.LIST_FORMAT_RIGHT,  colswidth[1])
        self.AppendColumn(colnames[2], wx.LIST_FORMAT_CENTER, colswidth[2])
        #self.SetMainColumn(0)
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        
        self.Data = data
        #self.Obj  = obj

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
        nodeData = self.GetData(n)
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
        nodeData = self.GetData(node)
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
            nodeAttr = self.GetItemData(node)
            attr = self.FmtItem if nodeAttr.Edit else self.FmtNoEdit
        else:
            attr = self.FmtGroup
            for i in item:
                self.UpdateFormats(i)
        
        fg, bg, bold = attr
        #self.SetItemTextColour(node, fg)
        #self.SetItemBackgroundColour(node, bg)
        #self.SetItemBold(node, bold)
    
    def UpdateValues(self, item=None, setEvent=False):
        if item is None:
            item = self._data
        
        if item.IsItem:
            n = self.GetNode(item)
            self.SetItemText(n, 1, item.GetText(self._obj))
            if setEvent:
                evt = myEvent(Id=self.GetId(), Ctrl=self, Item=item)
                self.GetEventHandler().ProcessEvent(evt)
        else:
            for i in item:
                self.UpdateValues(i, setEvent)
    
    #-------------------------------------------------------------------------------------
    # Private methos

    def _addNode(self, group):
        for i in group:
            #n = self.AppendItem(node, i.Name)
            n = self.InsertItem(self.GetItemCount(), i.Name)
            self.SetItem(n, 2, i.Unit)
            #self.SetItemData(n, _NodeData(i))
            fg, bg, bold = self.FmtItem
            #self.SetItemText(n, 2, i.Unit)
            #self.SetItemData(n, _NodeData(i))
            #self._nodeDict[id(i)] = n
            if not i.IsItem:
                fg, bg, bold = self.FmtGroup
                self._addNode(i)
            self.SetItemTextColour(n, fg)
            self.SetItemBackgroundColour(n, bg)
            #self.SetItemBold(n, bold)
    
    def _updateMsgBox(self, i): 
        if self._msgBox is None:
            return
        _value = i.GetText(self._obj) if i.IsItem else ""
        self._msgBox.SetText(i.Name, i.Msg, _value)

    #-------------------------------------------------------------------------------------
    # Properties methods
    
    @property
    def Data(self):
        return self._data
    
    @Data.setter
    def Data(self, value):
        self.DeleteAllItems()
        
        self._data = value
        #self._nodeDict = {} # relaciona items in EditorData con nodos
        
        #root = self.AddRoot(self._data.Name)
        #root = self.AppendItem(self.GetRootItem(), self._data.Name)
        #self._nodeDict[id(self._data)] = root
        
        self._addNode(self._data)
        #self.UpdateFormats()
        #self.Expand(root)
    
    @property
    def Obj(self):
        return self._obj
    
    @Obj.setter
    def Obj(self, value):
        if value is None:
            self._obj = self._data.CreateObj()
        else:
            self._obj = value
        self.UpdateValues()

    def _setMsgBox(self, value):
        self._msgBox = value
    MsgBox = property(None, _setMsgBox)