# CRISTIAN ECHEVERRÍA RABÍ

import sys
from datetime import datetime

#-----------------------------------------------------------------------------------------

__all__ = ['BaseData', 'RowData', 'ObjData']

#-----------------------------------------------------------------------------------------

def getAttrRec(obj, attr):
    """Devuelve atributo buscando recursivamente"""
    if attr is None:
        return ""
    val = obj
    for at in attr.split("."):
        val = getattr(val, at)
    return val


class CompareAttr(object):
    
    def __init__(self, typ, attr):
        self.default = ""
        if typ == "number":
            self.default = -sys.maxsize
        if typ == "datetime":
            self.default = datetime(1,1,1)
        self.attr = attr
    
    def getValue(self, obj):
        return getAttrRec(obj, self.attr)
    
    def __call__(self, x):
        vx = self.getValue(x)
        if vx is None: return self.default
        return vx


class CompareCol(CompareAttr):
    
    def getValue(self, obj):
        return obj[self.attr]


#-----------------------------------------------------------------------------------------

class BaseData(object):
    __slots__ = ()
    
    def __len__(self):
        return 10
    
    def __getitem__(self, key):
        txt = "Fila %d" % key
        return txt
    
    def getValue(self, row, header):
        txt = "Row %d, Col %s" % (row, header.text)
        return txt
    
    def toString(self, row, header):
        value = self.getValue(row, header)
        return header.toString(value)
    
    def sortByHeader(self, header):
        pass
    
    def reverse(self):
        pass

#-----------------------------------------------------------------------------------------

class RowData(list):
    __slots__ = () 
    
    def getValue(self, row, header):
        return self[row][header.pos]
    
    def toString(self, row, header):
        value = self.getValue(row, header)
        return header.toString(value)
    
    def sortByHeader(self, header):
        self.sort(key=CompareCol(header.typ, header.pos))

#-----------------------------------------------------------------------------------------

class ObjData(RowData):
    __slots__ = ()
    
    def getValue(self, row, header):
        return getAttrRec(self[row], header.attr)
    
    def sortByHeader(self, header):
        self.sort(key=CompareAttr(header.typ, header.attr))