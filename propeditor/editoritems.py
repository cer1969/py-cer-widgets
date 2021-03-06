# CRISTIAN ECHEVERRÍA RABÍ

from cer.value import validator
import cer.widgets.dialogs as dlg

#-----------------------------------------------------------------------------------------

__all__ = ['Group', 'Item', 'DataItem', 'Text', 'Float', 'Int', 'DateTime', 'Date', 
           'Time', 'Switch', 'Choice']

#-----------------------------------------------------------------------------------------

def _get_last_instance(obj, attr):
    # retorna la ultima instancia en attr string
    val = obj
    for at in attr.split(".")[:-1]:
        val = getattr(val, at)
    return val

#-----------------------------------------------------------------------------------------

class Group(object):
    """Header to separate items
    
    Public attributtes
    Name   : Name to display
    Msg    : Help message to display
    Unit   : Text for unit
    
    Read-only properties
    IsItem : False
    Edit   : False
    
    """
    
    __slots__ = ('Name', 'Msg', 'Unit', '_isitem', '_edit')
    
    def __init__(self, name, msg="", unit=""):
        self.Name = name
        self.Msg = msg
        self.Unit = unit
        self._isitem = False
        self._edit = False
    
    @property
    def IsItem(self):
        return self._isitem

    @property
    def Edit(self):
        return self._edit

#-----------------------------------------------------------------------------------------

class Item(Group):
    """Item for EditorData
    
    Public attributtes
    Attr   : Attribute name
    Getter : Getter object to change value
    Name   : Name to display, if None Name=Attr
    Edit   : True if item is editable. Initial value.
    Msg    : Help message to display
    Unit   : Text for unit
    
    Read-only properties
    IsItem : True
    
    """
    
    __slots__ = ('Attr', 'Getter')
    
    def __init__(self, attr, getter, name=None, edit=True, msg="", unit=""):
        _name = attr if name is None else name
        Group.__init__(self, _name, msg, unit)

        self.Attr = attr
        self.Getter = getter
        self._isitem = True
        self._edit = edit
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def GetText(self, obj):
        value = self.GetValue(obj)
        return self.Getter.GetText(value)
       
    def GetValue(self, obj):
        objAttr  = _get_last_instance(obj, self.Attr)
        attr = self.Attr.split(".")[-1]
        return getattr(objAttr, attr)
    
    def SetValue(self, obj, value):
        objAttr  = _get_last_instance(obj, self.Attr)
        attr = self.Attr.split(".")[-1]
        setattr(objAttr, attr, value)
    
    @property
    def Edit(self):
        return self._edit

    @Edit.setter
    def Edit(self, v):
        self._edit = v


#-----------------------------------------------------------------------------------------

class DataItem(Item):
    """Item para DataGetter"""
    __slots__ = ()
    
    def __init__(self, attr, val, name=None, ctrlSize=None, ctrlStyle=0, edit=True, 
                 msg="", unit=""):
        txt = "%s ?" % (attr if name is None else name)
        getter = dlg.DataGetter(val, txt, ctrlSize, ctrlStyle)
        Item.__init__(self, attr, getter, name, edit, msg, unit)


class Text(DataItem):
    __slots__ = ()
    
    def __init__(self, attr, name=None, ctrlSize=None, ctrlStyle=0, edit=True, 
                 msg="", unit=""):
        val = validator.Text()
        DataItem.__init__(self, attr, val, name, ctrlSize, ctrlStyle, edit, msg, unit)


class Float(DataItem):
    __slots__ = ()
    
    def __init__(self, attr, name=None, format="%.2f", vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=0, edit=True, msg="", unit=""):
        val = validator.Float(format, vmin, vmax)
        DataItem.__init__(self, attr, val, name, ctrlSize, ctrlStyle, edit, msg, unit)

class Int(DataItem):
    __slots__ = ()
    
    def __init__(self, attr, name=None, format="%d", vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=0, edit=True, msg="", unit=""):
        val = validator.Int(format, vmin, vmax)
        DataItem.__init__(self, attr, val, name, ctrlSize, ctrlStyle, edit, msg, unit)

#-----------------------------------------------------------------------------------------

class DateTime(Item):
    __slots__ = ()

    def __init__(self, attr, name=None, format=None, vmin=None, vmax=None, ctrlSize=None,
                 ctrlStyle=None, useSecs=False, edit=True, msg="", unit=""):
        txt = "%s ?" % (attr if name is None else name)
        getter = dlg.DateTimeGetter(txt, format, vmin, vmax, ctrlSize, ctrlStyle, useSecs)
        Item.__init__(self, attr, getter, name, edit, msg, unit)


class Date(Item):
    __slots__ = ()

    def __init__(self, attr, name=None, format=None, vmin=None, vmax=None, ctrlSize=None,
                 ctrlStyle=None, edit=True, msg="", unit=""):
        txt = "%s ?" % (attr if name is None else name)
        getter = dlg.DateGetter(txt, format, vmin, vmax, ctrlSize, ctrlStyle)
        Item.__init__(self, attr, getter, name, edit, msg, unit)


class Time(Item):
    __slots__ = ()
    
    def __init__(self, attr, name=None, format=None, vmin=None, vmax=None, useSecs=None,
                 edit=True, msg="", unit=""):
        txt = "%s ?" % (attr if name is None else name)
        getter = dlg.TimeGetter(txt, format, vmin, vmax, useSecs)
        Item.__init__(self, attr, getter, name, edit, msg, unit)

#-----------------------------------------------------------------------------------------

class Switch(Item):
    __slots__ = ()
    
    def __init__(self, attr, choices, name=None, getText=None, edit=True, 
                 msg="", unit=""):
        getter = dlg.SwitchGetter(choices, getText)
        Item.__init__(self, attr, getter, name, edit, msg, unit)


class Choice(Item):
    __slots__ = ()
    
    def __init__(self, attr, choices, name=None, getText=None, edit=True,
                 msg="", unit=""):
        txt = "%s ?" % (attr if name is None else name)
        getter = dlg.ChoiceGetter(choices, txt, getText)
        Item.__init__(self, attr, getter, name, edit, msg, unit)

#-----------------------------------------------------------------------------------------