# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

#-----------------------------------------------------------------------------------------

__all__ = ['BaseObj', 'EditorGroup', 'EditorData']

#-----------------------------------------------------------------------------------------

#class BaseObj(object):
#    def __init__(self, names):
#        for i in names:
#            setattr(self, i, None)

class BaseObj(dict):
    
    def __init__(self, names):
        dict.__init__(self)
        for i in names:
            self[i] = None
    
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

#-----------------------------------------------------------------------------------------

class EditorGroup(list):
    """List object to collect Item and others EditorData
    
    Write-only properties
    Edit   : If True all appened items will be editable. Initial value.
             WARNING: This does not affect items appened after calling Edit = value
    
    Read-only properties
    IsItem : False
    
    """
    
    __slots__ = ('Name', 'Msg', "Unit")
    
    def __init__(self, name, msg, *items):
        list.__init__(self, items)
        self.Name = name
        self.Msg = msg
        self.Unit = ""
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def GetAttrList(self):
        """Return a list with attr names"""
        names = []
        for i in self:
            if i.IsItem:
                names.append(i.Attr)
            else:
                names = names + i.GetAttrList()
        return names
    
    def CreateObj(self):
        """Create a BaseObj with attr names
        It does not work with nested objects
        """
        return BaseObj(self.GetAttrList())
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _getEdit(self):
        return None
    
    def _setEdit(self, value=True):
        for i in self:
            i.Edit = value
    
    def _getIsItem(self):
        return False
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    Edit   = property(_getEdit, _setEdit)
    IsItem = property(_getIsItem)

#-----------------------------------------------------------------------------------------

class EditorData(EditorGroup):
    """EditorGroup for the root object"""

    __slots__ = ()
    
    def __init__(self, *items):
        EditorGroup.__init__(self, "root", "", *items)