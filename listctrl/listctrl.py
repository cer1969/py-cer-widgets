# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx
import wx.lib.newevent

#-----------------------------------------------------------------------------------------

__all__ = ['ListCtrl', 'LISTCTRL_DEF_STYLE', 'EVTC_LISTCTRL_DATACHANGE']

#-----------------------------------------------------------------------------------------

myEvent, EVTC_LISTCTRL_DATACHANGE = wx.lib.newevent.NewEvent()

LISTCTRL_DEF_STYLE = wx.LC_VRULES|wx.LC_SINGLE_SEL

#-----------------------------------------------------------------------------------------

class ListCtrl(wx.ListCtrl):

    def __init__(self, parent, manager, size=(-1,-1), sortByCol=True, 
                 style=LISTCTRL_DEF_STYLE):
        """
        manager   : DataManager object
        size      : ListCtrl size
        sortByCol : If true activate column sorting
        style     : ListCtrl styles
        """
        style = wx.LC_VIRTUAL|wx.LC_REPORT|style
        
        wx.ListCtrl.__init__(self, parent, -1, size=size, style=style)
        
        self.SetImageList(wx.ImageList(1, 1))
        
        self.Manager = manager
        
        for i, header in enumerate(self.Manager):
            self.InsertColumn(i, header.Name, header.Align, header.Width)
        
        self.Attrs = [None,None]
        self._data  = None
        self._selected = None
        self._currentSort = None
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,   self.OnItemSelected,   self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self.OnItemActivated,  self)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self)
        if sortByCol:
            self.Bind(wx.EVT_LIST_COL_CLICK,   self.OnColClick,       self)

    #--------------------------------------------------------------------------
    # Propiedad Data
    def _getData(self):
        return self._data

    def _setData(self, value):
        self._data = value
        self._currentSort = None
        self.SortByCol()
        evt = myEvent(Id=self.GetId(), Ctrl=self)
        self.GetEventHandler().ProcessEvent(evt)

    Data = property(_getData, _setData)

    #-------------------------------------------------------------------------------------
    # Utilidades
    
    def SetColumnText(self, pos, text):
        c = self.GetColumn(pos)
        c.SetText(text)
        self.SetColumn(pos, c)
    
    def SetImageList(self, imageList, which=wx.IMAGE_LIST_SMALL):
        # Se sobreescribe SetImageList para guardar referencia a la lista de imagenes
        self.__imageList = imageList
        wx.ListCtrl.SetImageList(self, self.__imageList, which)
    
    #-------------------------------------------------------------------------------------
    # Propiedad Selection y eventos asociados
    
    def _getSelection(self):
        return self._selected

    def _setSelection(self,item=None):
        if not(item is None):
            if self.GetNumberRows() > item:
                self.SetItemState(item, wx.LIST_STATE_SELECTED,#|wx.LIST_STATE_FOCUSED,
                                        wx.LIST_STATE_SELECTED)#|wx.LIST_STATE_FOCUSED)
                self.EnsureVisible(item)
            else:
                item = None
        self._selected = item
    
    Selection = property(_getSelection, _setSelection)

    #-------------------------------------------------------------------------------------
    
    def OnItemSelected(self,event):
        self._selected = event.GetIndex()
        event.Skip()

    def OnItemActivated(self,event):
        self._selected = event.GetIndex()
        event.Skip()

    def OnItemDeselected(self,event):
        self._selected = None
        event.Skip()

    def OnColClick(self, event):
        col = event.GetColumn()
        if col == self._currentSort:
            self.Manager.DataReverse(self._data)
            self.UpdateView()
        else:
            self.SortByCol(col)
            self._currentSort = col
        event.Skip()

    def SortByCol(self, col=None):
        # No modifica __currentSort
        # Si col es None se repite último sort
        if col is None:
            col = self._currentSort
        if not(col is None):
            self.Manager.DataSort(self._data, col)
        self.UpdateView()
    
    def UpdateColsWidth(self):
        for i, header in enumerate(self.Manager):
            self.SetColumnWidth(i, header.Width)
    
    #-------------------------------------------------------------------------------------
    # Actualiza la vista de los item
    
    def UpdateView(self):
        """ Normalmente este método no requiere sobreescritura
        """
        numberRows = self.GetNumberRows()
        self.SetItemCount(numberRows)
        if numberRows <=0:
            self.Selection = None
        else:
            ini = self.GetTopItem()
            fin = ini + 1 + self.GetCountPerPage()
            self.RefreshItems(ini, fin)
            if self.Selection is None:
                self.Selection = 0
            elif self.Selection > numberRows - 1:
                self.Selection = numberRows - 1
            else:
                # Necesario para forzar repintado de la selección
                self.Selection = self.Selection
        self.Refresh()
    
    #-------------------------------------------------------------------------------------
    # Métodos personalizables de la lista virtual
    
    def GetNumberRows(self):
        return self.Manager.GetNumberRows(self._data)
    
    def OnGetItemText(self,row,col):
        return self.Manager.GetItemText(self._data, row, col)

    def OnGetItemImage(self,row):
        return -1 

    def OnGetItemAttr(self,row):
        return self.Attrs[row % 2]
        