# CRISTIAN ECHEVERRÍA RABÍ

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
    
    def __init__(self, attr):
        self.attr = attr
    
    def getValue(self, obj):
        return getAttrRec(obj, self.attr)
    
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
        self.sort(CompareCol(header.pos))

#-----------------------------------------------------------------------------------------

class ObjData(RowData):
    __slots__ = ()
    
    def getValue(self, row, header):
        return getAttrRec(self[row], header.attr)
    
    def sortByHeader(self, header):
        self.sort(CompareAttr(header.attr))