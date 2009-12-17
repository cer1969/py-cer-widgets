# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import cer.utils.validators as cval
import cer.widgets.dialogs as dlg

#-----------------------------------------------------------------------------------------

__all__ = ['Item', 'DataItem', 'Text', 'Float', 'Int', 'DateTime', 'Date', 'Time',
           'Switch', 'Choice']

#-----------------------------------------------------------------------------------------

def _get_last_instance(obj, attr):
    # retorna la ultima instancia en attr string
    val = obj
    for at in attr.split(".")[:-1]:
        val = getattr(val, at)
    return val

#-----------------------------------------------------------------------------------------

class Item(object):
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
    
    __slots__ = ('Attr', 'Getter', 'Name', 'Edit', 'Msg', 'Unit')
    
    def __init__(self, attr, getter, name=None, edit=True, msg="", unit=""):
        self.Attr = attr
        self.Getter = getter
        self.Name = attr if name is None else name
        self.Edit = edit
        self.Msg = msg
        self.Unit = unit
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def GetText(self, obj):
        value = self.GetValue(obj)
        return self.Getter.GetText(value)
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def GetValue(self, obj):
        objAttr  = _get_last_instance(obj, self.Attr)
        attr = self.Attr.split(".")[-1]
        return getattr(objAttr, attr)
    
    def SetValue(self, obj, value):
        objAttr  = _get_last_instance(obj, self.Attr)
        attr = self.Attr.split(".")[-1]
        setattr(objAttr, attr, value)
    
    def _getIsItem(self):
        return True
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    IsItem = property(_getIsItem)


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
        val = cval.TextValidator()
        DataItem.__init__(self, attr, val, name, ctrlSize, ctrlStyle, edit, msg, unit)


class Float(DataItem):
    __slots__ = ()
    
    def __init__(self, attr, name=None, format="%.2f", vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=0, edit=True, msg="", unit=""):
        val = cval.FloatValidator(format, vmin, vmax)
        DataItem.__init__(self, attr, val, name, ctrlSize, ctrlStyle, edit, msg, unit)

class Int(DataItem):
    __slots__ = ()
    
    def __init__(self, attr, name=None, format="%d", vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=0, edit=True, msg="", unit=""):
        val = cval.IntValidator(format, vmin, vmax)
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