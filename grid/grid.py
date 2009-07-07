# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import wx
import wx.grid as grid

#-----------------------------------------------------------------------------------------

__all__ = ['Grid', 'ENTER_MOVE_RIGHT', 'ENTER_MOVE_DOWN', 'ENTER_MOVE_NEXTEDIT']

#-----------------------------------------------------------------------------------------

TableMessage = grid.GridTableMessage
TABLE_NOTIFY_ROWS_APPENDED = grid.GRIDTABLE_NOTIFY_ROWS_APPENDED
#TABLE_NOTIFY_ROWS_INSERTED = grid.GRIDTABLE_NOTIFY_ROWS_INSERTED
TABLE_NOTIFY_ROWS_DELETED  = grid.GRIDTABLE_NOTIFY_ROWS_DELETED
TABLE_NOTIFY_COLS_APPENDED = grid.GRIDTABLE_NOTIFY_COLS_APPENDED
#TABLE_NOTIFY_COLS_INSERTED = grid.GRIDTABLE_NOTIFY_COLS_INSERTED
TABLE_NOTIFY_COLS_DELETED  = grid.GRIDTABLE_NOTIFY_COLS_DELETED

ENTER_MOVE_RIGHT    = 0
ENTER_MOVE_DOWN     = 1
ENTER_MOVE_NEXTEDIT = 2

#-----------------------------------------------------------------------------------------

class Grid(grid.Grid):
    # datamodel: Objeto cg.GridDataModel
    # size: Size de la grid
    def __init__(self, parent, datamodel, size=(300,300)):
        grid.Grid.__init__(self,parent,-1,size=size,style=wx.SUNKEN_BORDER)

        self._nrows = 0
        self._ncols = 0
        self.DataModel = datamodel
        self.AutoAddRows = False
        self.EnterMove = ENTER_MOVE_RIGHT
        
        # Igualamos fonts de celdas y labels
        f = self.GetDefaultCellFont()
        self.SetLabelFont(f)
        
        self.SetRowLabelAlignment(wx.CENTER,wx.CENTER)
        self.SetColLabelAlignment(wx.CENTER,wx.CENTER)
        self.SetGridLineColour("GRAY80")
        
        self.SetMargins(0,0)
        
        self.SetSelectionBackground("LIGHT BLUE")
        self.SetSelectionForeground("BLUE")
        self.SetSelectionMode(grid.Grid.wxGridSelectCells)
        
        grid.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)
        wx.EVT_KEY_DOWN(self, self.OnKeyDown)

    #-------------------------------------------------------------------------------------
    # Propiedad DataModel
    def GetDataModel(self):
        return self.GetTable()

    def SetDataModel(self,datamodel): 
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(datamodel,True)
        self._nrows = datamodel.GetNumberRows()
        self._ncols = datamodel.GetNumberCols()

    DataModel = property(GetDataModel,SetDataModel)

    #-------------------------------------------------------------------------------------
    
    def SetRowLabelWidthInChars(self, nchars, dpixels=6):
        w,h,d,e = self.GetFullTextExtent(nchars*"0",self.GetLabelFont())
        self.SetRowLabelSize(w+dpixels)

    def SetColLabelHeightInChars(self, nchars, dpixels=4):
        w,h,d,e = self.GetFullTextExtent("0",self.GetLabelFont())
        self.SetColLabelSize(nchars*h+dpixels+d+e+dpixels)

    def SetColWidthInChars(self, col, nchars, dpixels=6):
        w,h,d,e = self.GetFullTextExtent(nchars*"0",self.GetDefaultCellFont())
        self.SetColSize(col,w+dpixels)
    
    def GetColWidthInChars(self, col, dpixels=6):
        wc = self.GetColSize(col) - dpixels
        w,h,d,e = self.GetFullTextExtent("0",self.GetDefaultCellFont())
        return round(wc/w,0)
    
    #def SetDefaultColSizeInChars(self,nchars):
    #    w,h,d,e = self.GetFullTextExtent(nchars*"0",self.GetDefaultCellFont())
    #    self.SetDefaultColSize(w+5,True)
    
    #-------------------------------------------------------------------------------------
    
    def OnKeyDown(self, evt):
        if evt.KeyCode not in (wx.WXK_RETURN,wx.WXK_NUMPAD_ENTER):
            evt.Skip()
            return

        if evt.ControlDown():   # the edit control needs this key
            evt.Skip()
            return

        self.DisableCellEditControl()
        
        if self.EnterMove == ENTER_MOVE_RIGHT:
            success = self.MoveToRightCell()
        elif self.EnterMove == ENTER_MOVE_DOWN:
            success = self.MoveCursorDown(False)
        else:
            success = self.MoveToNextEditableCell()
        
        if success:
            return
        
        if self.AutoAddRows:
            self.AppendRows(1)
            row = self.DataModel.GetNumberRows() - 1
            col = self.GetGridCursorCol() if (self.EnterMove == ENTER_MOVE_DOWN) else 0
            self.SetGridCursor(row, col)
            self.MakeCellVisible(row, col)
            if self.EnterMove == ENTER_MOVE_NEXTEDIT:
                self.MoveToNextEditableCell()

    def MoveToRightCell(self):
        success = self.MoveCursorRight(False)
        if success:
            return True
        row = self.GetGridCursorRow() + 1
        if row < self.DataModel.GetNumberRows():
            self.SetGridCursor(row, 0) 
            self.MakeCellVisible(row, 0)
            return True
        return False
        
    def MoveToNextEditableCell(self):
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        flag = True
        while flag:
            col = col + 1
            if col > (self.DataModel.GetNumberCols() - 1):
                col = 0
                row = row + 1
                if row > (self.DataModel.GetNumberRows() - 1):
                    return False
            if self.IsReadOnly(row,col)==False:
                self.SetGridCursor(row,col)
                self.MakeCellVisible(row,col)
                flag = False
        return True

    #-------------------------------------------------------------------------------------
    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    #-------------------------------------------------------------------------------------
    # Sobre-escribiendo métodos
    
    def AppendRows(self,numRows=1):
        op = grid.Grid.AppendRows(self,numRows)
        self.UpdateRowsView()
        return op

    def DeleteRows(self,pos=0,numRows=1):
        op = grid.Grid.DeleteRows(self,pos,numRows)
        self.UpdateRowsView()
        return op

    def InsertRows(self,pos=0,numRows=1):
        op = grid.Grid.InsertRows(self,pos,numRows)
        self.UpdateRowsView()
        return op
    
    #-------------------------------------------------------------------------------------
    # Métodos CER
    
    def UpdateColsView(self):
        rnnew = self.DataModel.GetNumberCols()
        rnold = self._ncols
        dif = rnnew - rnold
        if dif == 0:
            self.Refresh()
            return
        if dif > 0:
            msg = TableMessage(self.DataModel,
                               TABLE_NOTIFY_COLS_APPENDED,
                               dif)
        else:
            msg = TableMessage(self.DataModel,
                               TABLE_NOTIFY_COLS_DELETED,
                               0,
                               -dif)
        self.ProcessTableMessage(msg)
        self._ncols = rnnew
    
    def UpdateRowsView(self):
        rnnew = self.DataModel.GetNumberRows()
        rnold = self._nrows
        dif = rnnew - rnold
        if dif == 0:
            self.Refresh()
            return
        if dif > 0:
            msg = TableMessage(self.DataModel,
                               TABLE_NOTIFY_ROWS_APPENDED,
                               dif)
        else:
            msg = TableMessage(self.DataModel,
                               TABLE_NOTIFY_ROWS_DELETED,
                               0,
                               -dif)
        self.ProcessTableMessage(msg)
        self._nrows = rnnew
    
    def AppendRowsData(self,data):
        self.DataModel.AppendRowsData(data)
        self.UpdateRowsView()
        
    def InsertRowsData(self,pos,data):
        self.DataModel.InsertRowsData(pos,data)
        self.UpdateRowsView()

    def InsertSelectedRows(self):
        filas = self.GetSelectedRows()
        numRows = len(filas)
        if numRows == 0: return 
        pos = filas[0]
        self.InsertRows(pos,numRows)
        
    def DeleteSelectedRows(self):
        filas = self.GetSelectedRows()
        numRows = len(filas)
        if numRows == 0: return
        pos = filas[0]
        self.DeleteRows(pos,numRows)

    def ReplaceData(self,data):
        self.DataModel.Data = data
        self.UpdateRowsView()
        self.UpdateColsView()

    def ValidateData(self):
        return self.DataModel.ValidateData()