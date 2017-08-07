# CRISTIAN ECHEVERRÍA RABÍ

#-----------------------------------------------------------------------------------------

__all__ = ['BaseObj', 'EditorData']

#-----------------------------------------------------------------------------------------

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

class EditorData(list):
    """List object to collect Item
    
    Write-only properties
    Edit   : If True all appened items will be editable. Initial value.
             WARNING: This does not affect items appened after calling Edit = value
    """
    __slots__ = ()
    
    def __init__(self, *items):
        list.__init__(self, items)
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def GetAttrList(self):
        """Return a list with attr names"""
        names = []
        for item in self:
            if item.IsItem:
                names.append(item.Attr)
        return names
    
    def CreateObj(self):
        """Create a BaseObj with attr names
        It does not work with nested objects
        """
        return BaseObj(self.GetAttrList())
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    @property
    def Edit(self):
        return None
    
    @Edit.setter
    def Edit(self, value=True):
        for item in self:
            if item.IsItem:
                item.Edit = value