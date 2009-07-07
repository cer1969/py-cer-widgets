# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import wx
import wx.grid as grid

#-----------------------------------------------------------------------------------------

__all__ = ['Header', 'DataModel', 'TableDataModel',
           'VALUE_STRING', 'VALUE_FLOAT', 'VALUE_NUMBER', 'VALUE_BOOL', 'VALUE_CHOICE'
           ]

#-----------------------------------------------------------------------------------------

VALUE_STRING = grid.GRID_VALUE_STRING
VALUE_FLOAT = grid.GRID_VALUE_FLOAT
VALUE_NUMBER = grid.GRID_VALUE_NUMBER
VALUE_BOOL = grid.GRID_VALUE_BOOL
VALUE_CHOICE = grid.GRID_VALUE_CHOICE

#-----------------------------------------------------------------------------------------

def GridBool(value):
    val = bool(value)
    if val: return 1
    else: return 0

DEFAULT = {}
DEFAULT[VALUE_STRING] = (str,"")
DEFAULT[VALUE_FLOAT]  = (float,0.0)
DEFAULT[VALUE_NUMBER] = (int,0)
DEFAULT[VALUE_BOOL]   = (GridBool,0)
DEFAULT[VALUE_CHOICE] = (str,"")

#-----------------------------------------------------------------------------------------
# Class Header

class Header(object):
    def __init__(self,name,type=VALUE_STRING,
                           defval=None,
                           func=None,
                           args=None):

        self.name   = name
        self.type   = type

        if defval is None:
            defval = DEFAULT[self.type][1]
        if func is None:
            func = DEFAULT[self.type][0]

        self.defval = defval
        self.func   = func
        self.args   = args

#-----------------------------------------------------------------------------------------
# Class DataModel

class DataModel(grid.PyGridTableBase):
    def __init__(self):
        grid.PyGridTableBase.__init__(self)

    #-------------------------------------------------------------------------------------
    # Métodos requeridos por wx.PyGridTableBase

    def GetNumberRows(self):
        return 10

    def GetNumberCols(self):
        return 10

    def IsEmptyCell(self,row,col):
        return False

    def GetValue(self,row,col):
        return "%d,%d" % (row,col)

    def SetValue(self, row, col, value):
        # Se debe sobreescribir
        pass

    def GetColLabelValue(self, col):
        return "Columna %d" % col

    def GetRowLabelValue(self, row):
        return "%d" % row

    # Llamada para determinar tipo de editor/renderer a usar
    def GetTypeName(self,row,col):
        return VALUE_STRING

    # Llamada para determinar como la data puede ser obtenida y guardada por el
    # editor/renderer.
    def CanGetValueAs(self,row,col,typeName):
        colType = self.GetTypeName(row,col).split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self,row,col,typeName):
        return self.CanGetValueAs(row,col,typeName)

    #-------------------------------------------------------------------------------------
    # Métodos Cer para SobreEscribir

    def ValidateData(self):
        return True


#-----------------------------------------------------------------------------------------
# Class TableDataModel
# DataModel basado en tabla de datos

class TableDataModel(DataModel):
    
    def __init__(self,headers=[]):
        DataModel.__init__(self)
        self.Headers = headers
        self.__data = []

    #-------------------------------------------------------------------------------------
    # Propiedad data
    
    def GetData(self):
        return self.__data
        
    def SetData(self,data):
        data = self.GetCheckedData(data)
        self.__data = data

    Data = property(GetData,SetData)

    #-------------------------------------------------------------------------------------
    # Métodos SobreEscritos de DataModel

    def GetNumberRows(self):
        return len(self.Data)

    def GetNumberCols(self):
        return len(self.Headers)

    def IsEmptyCell(self,row,col):
        return not self.Data[row][col]

    def GetValue(self,row,col):
        return self.Data[row][col]

    def SetValue(self,row,col,value):
        self.Data[row][col] = value

    def GetColLabelValue(self,col):
        header = self.Headers[col]
        return header.name
    
    def GetTypeName(self,row,col):
        header = self.Headers[col]
        typeName = header.type
        if not(header.args is None):
            typeName = "%s:%s" % (typeName,header.args)
        return typeName

    #--------------------------------------------------
    
    def AppendRows(self,numRows=1):
        defValues = [header.defval for header in self.Headers]
        data = numRows*[defValues]
        for i in data:
            self.__data.append(i)

    def DeleteRows(self,pos=0,numRows=1):
        del(self.__data[pos:pos+numRows])

    def InsertRows(self,pos=0,numRows=1):
        defValues = [header.defval for header in self.Headers]
        data = numRows*[defValues]
        for i in data:
            self.__data.insert(pos,i)

    #--------------------------------------------------
    # Métodos CER

    def AppendRowsData(self,data):
        data = self.GetCheckedData(data)
        for i in data:
            self.__data.append(i)

    def InsertRowsData(self,pos,data):
        data = self.GetCheckedData(data)
        #numRows = len(data)
        self.__data[pos:pos] = data
        #data.reverse()
        #for i in data:
        #    self.__data.insert(pos,i)

    def GetCheckedData(self,data):
        ncols = self.GetNumberCols()
        sal = []
        for row in data:
            if len(row) < ncols:
                row = row + (ncols - len(row))*[""]
            fila = []
            for i,x in enumerate(row):
                if i < ncols:
                    header = self.Headers[i] 
                    try:
                        val = header.func(row[i])
                    except ValueError:
                        val = header.defval
                else:
                    val = x
                fila.append(val)
            sal.append(fila) 
        return sal