# CRISTIAN ECHEVERRÍA RABÍ

import wx
import wx.lib.newevent

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
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        
        self.Data = data
        self.Obj  = obj

    #-------------------------------------------------------------------------------------
    # Events
    
    def OnItemActivated(self, event):
        n = event.GetIndex()
        item = self._data[n]
        self.EditItem(item)
        event.Skip()
    
    def OnItemSelected(self, event):
        if self._msgBox is None:
            return
        n = event.GetIndex()
        item = self._data[n]
        self._updateMsgBox(item)
        event.Skip()
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def SetEdit(self, item, edit):
        if item.IsItem:
            item.Edit = edit
        self.UpdateFormat(item)
    
    #def Edit(self, item):
    #    node = self.GetNode(item)
    #    self.EditNode(node)

    def EditItem(self, item):
        if not item.IsItem:
            return
        if not item.Edit:
            return
        
        cur_value = item.GetValue(self._obj)
        new_value = item.Getter(self, cur_value)
        if new_value is None:
            return
        if new_value == cur_value:
            return
        item.SetValue(self._obj, new_value)
        self.UpdateValue(item, setEvent=True)
        self._updateMsgBox(item)
    
    def UpdateView(self):
        self.UpdateValues()
        self.UpdateFormats()

    def UpdateFormats(self):
        for item in self._data:
            self.UpdateFormat(item)
    
    def UpdateFormat(self, item):
        attr = self.FmtGroup
        if item.IsItem:
            attr = self.FmtItem if item.Edit else self.FmtNoEdit
        
        fg, bg, bold = attr
        
        n = self._data.index(item)

        self.SetItemTextColour(n, fg)
        self.SetItemBackgroundColour(n, bg)
        if bold:
            f = self.GetItemFont(n)
            self.SetItemFont(n, f.Bold())
    
    def UpdateValues(self, setEvent=False):
        for item in self._data:
            self.UpdateValue(item, setEvent)
    
    def UpdateValue(self, item, setEvent=False):
        if item.IsItem:
            n = self._data.index(item)
            self.SetItem(n, 1, item.GetText(self._obj))
            if setEvent:
                evt = myEvent(Id=self.GetId(), Ctrl=self, Item=item)
                self.GetEventHandler().ProcessEvent(evt)
    
    #-------------------------------------------------------------------------------------
    # Private methos
    
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
    def Data(self, data):
        self._data = data

        self.DeleteAllItems()
        
        for item in data:
            n = self.InsertItem(self.GetItemCount(), item.Name)
            self.SetItem(n, 2, item.Unit)
        self.UpdateFormats()
    
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