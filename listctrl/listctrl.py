# CRISTIAN ECHEVERRÍA RABÍ

import weakref
import wx
from wx.lib.newevent import NewEvent

#-----------------------------------------------------------------------------------------

__all__ = ['ListCtrl', 'LISTCTRL_DEF_STYLE', 'EVTC_LISTCTRL_DATACHANGE']

#-----------------------------------------------------------------------------------------

myEvent, EVTC_LISTCTRL_DATACHANGE = NewEvent()
LISTCTRL_DEF_STYLE = wx.LC_VRULES|wx.LC_SINGLE_SEL

#-----------------------------------------------------------------------------------------

class ListCtrl(wx.ListCtrl):

    def __init__(self, parent, headers, size=(-1,-1), style=LISTCTRL_DEF_STYLE):
        """
        headers : Headers objects list
        size  : ListCtrl size
        style : ListCtrl styles
        """
        style = wx.LC_VIRTUAL|wx.LC_REPORT|style
        
        wx.ListCtrl.__init__(self, parent, -1, size=size, style=style)
        
        self.SetImageList(wx.ImageList(1, 1))
        
        ctrl = weakref.proxy(self)
        for i, header in enumerate(headers):
            header.insert(i, ctrl)
        self.headers = headers
        
        self.attrs = [None, None]
        self._selected = None
        self._currentSort = None
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,   self._onItemSelected,   self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self._onItemActivated,  self)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._onItemDeselected, self)
        self.Bind(wx.EVT_LIST_COL_CLICK,       self._onColClick,       self)

    #-------------------------------------------------------------------------------------
    # Métodos sobreescritos
    
    def SetImageList(self, imageList, which=wx.IMAGE_LIST_SMALL):
        # Se sobreescribe SetImageList para guardar referencia a la lista de imagenes
        self._imageList = imageList
        wx.ListCtrl.SetImageList(self, self._imageList, which)
    
    # Métodos personalizables de la lista virtual
    
    def OnGetItemText(self, row, col):
        return self._data.toString(row, self.headers[col])
    
    def OnGetItemImage(self, row):
        return -1
    
    def OnGetItemAttr(self, row):
        return self.attrs[row % 2]

    #-------------------------------------------------------------------------------------
    # Métodos públicos
    
    def SortByCol(self, col=None):
        # No modifica __currentSort
        # Si col es None se repite último sort
        if col is None:
            col = self._currentSort
        if not(col is None):
            self._data.sortByHeader(self.headers[col])
        self.UpdateView()
    
    def UpdateView(self):
        """ Normalmente este método no requiere sobreescritura
        """
        nr = len(self._data)
        self.SetItemCount(nr)
        if nr <=0:
            self.selection = None
        else:
            ini = self.GetTopItem()
            fin = ini + 1 + self.GetCountPerPage()
            self.RefreshItems(ini, fin)
            if self.selection is None:
                self.selection = 0
            elif self.selection > nr - 1:
                self.selection = nr - 1
            else:
                # Necesario para forzar repintado de la selección
                self.selection = self.selection
        self.Refresh()
    
    #-------------------------------------------------------------------------------------
    # Propiedad data
    
    def _getData(self):
        return self._data
    
    def _setData(self, value):
        self._data = value
        self._currentSort = None
        self.SortByCol()
        evt = myEvent(idx=self.GetId(), ctrl=self)
        self.GetEventHandler().ProcessEvent(evt)
    
    data = property(_getData, _setData)
    
    #-------------------------------------------------------------------------------------
    # Propiedad selection y eventos asociados
    
    def _getSelection(self):
        return self._selected
    
    def _setSelection(self,item=None):
        if not(item is None):
            if len(self._data) > item:
                self.SetItemState(item, wx.LIST_STATE_SELECTED,#|wx.LIST_STATE_FOCUSED,
                                        wx.LIST_STATE_SELECTED)#|wx.LIST_STATE_FOCUSED)
                self.EnsureVisible(item)
            else:
                item = None
        self._selected = item
    
    selection = property(_getSelection, _setSelection)
    
    #-------------------------------------------------------------------------------------
    # Propiedad selectedItem
    
    def _getSelectedItem(self):
        if self._selected is None:
            return None
        else:
            return self._data[self._selected]
    
    selectedItem = property(_getSelectedItem)
    
    #-------------------------------------------------------------------------------------
    # Eventos 
    
    def _onItemSelected(self, event):
        self._selected = event.GetIndex()
        event.Skip()
    
    def _onItemActivated(self, event):
        self._selected = event.GetIndex()
        event.Skip()
    
    def _onItemDeselected(self, event):
        self._selected = None
        event.Skip()
    
    def _onColClick(self, event):
        col = event.GetColumn()
        if col == self._currentSort:
            self._data.reverse()
        else:
            self._data.sortByHeader(self.headers[col])
            self._currentSort = col
        self.UpdateView()
        event.Skip()