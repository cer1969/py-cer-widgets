# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

#-----------------------------------------------------------------------------------------

__all__ = ['DataManager', 'RowDataManager', 'ObjDataManager']

#-----------------------------------------------------------------------------------------

def getattr_rec(obj, attr):
    """Devuelve atributo buscando recursivamente"""
    if attr is None:
        return ""
    val = obj
    for at in attr.split("."):
        val = getattr(val,at)
    return val


class _compare_attr(object):
    
    def __init__(self, attr):
        self.attr = attr
    
    def getValue(self, obj):
        return getattr_rec(obj, self.attr)
    
    def __call__(self, x, y):
        vx = self.getValue(x)
        vy = self.getValue(y)
        if (vx is None) and (vy is None):
            return 0
        elif (vx is None) and not(vy is None):
            return -1
        elif not(vx is None) and (vy is None):
            return 1
        else:
            return cmp(vx, vy)


class _compare_col(_compare_attr):
    
    def getValue(self, obj):
        return obj[self.attr]


#-----------------------------------------------------------------------------------------

class DataManager(list):
    __slots__ = ()
    
    def __init__(self, *args):
        """
        args : Tuple with headers objects
        """
        list.__init__(self, args)
    
    def GetNumberRows(self, data):
        raise NotImplementedError

    def GetItemText(self, data, row, col):
        return "%d,%d" % (row,col)

    def DataSort(self, data, col, reverse=False):
        pass

    def DataReverse(self, data):
        pass

#-----------------------------------------------------------------------------------------

class RowDataManager(DataManager):
    __slots__ = ()
    
    def GetNumberRows(self, data):
        return len(data)

    def GetItemText(self, data, row, col):
        value = data[row][col]
        header = self[col]
        return header.GetText(value)

    def DataSort(self, data, col):
        data.sort(_compare_col(col))

    def DataReverse(self, data):
        data.reverse()

#-----------------------------------------------------------------------------------------

class ObjDataManager(RowDataManager):
    __slots__ = ()

    def GetItemText(self, data, row, col):
        obj = data[row]
        header = self[col]
        value = getattr_rec(obj, header.Attr)
        return header.GetText(value)

    def DataSort(self, data, col):
        attr = self[col].Attr
        data.sort(_compare_attr(attr))