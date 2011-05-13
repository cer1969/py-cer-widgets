# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx
from cer.widgets.controls.datactrl import DataCtrl

#-----------------------------------------------------------------------------------------

__all__ = ['DataDialog', 'DataGetter']

#-----------------------------------------------------------------------------------------

class DataDialog(wx.Dialog):
    """Simple dialog with DataCtrl for validation"""

    def __init__(self, parent, validator, title="Data Dialog", data=None, ctrlSize=None,
                 ctrlStyle=0, msg=None): 
        """
        validator : Validator object (cer.value.validator)
        title     : Dialog Title
        data      : Data value
        ctrlSize  : Size for DataCtrl
        ctrlStyle : Style for DataCtrl
        msg       : Message to display. Default to title
        """
        wx.Dialog.__init__(self, parent, -1, title)
        
        _size = (-1, -1) if ctrlSize is None else ctrlSize
        _msg = title if msg is None else msg
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        st = wx.StaticText(self, -1, _msg)
        box.Add(st, 0, wx.EXPAND|wx.ALL, 10)
        
        self._ctrl = DataCtrl(self, validator, data, _size, ctrlStyle)
        
        box.Add(self._ctrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        okbut = wx.Button(self, wx.ID_OK, "Ok")
        okbut.SetDefault()
        oksizer.Add(okbut, 0, wx.RIGHT, 10)
        oksizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 0)
        box.Add(oksizer, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        box.Fit(self)
        box.SetSizeHints(self)
        
        self.CentreOnParent(wx.BOTH)
    
    def _getData(self):
        return self._ctrl.data
    
    Data = property(_getData)

#-----------------------------------------------------------------------------------------

class DataGetter(object):
    """Callable: Show DataDialog and returns value"""
    
    __slots__ = ('_cerval', 'Title', 'Msg', 'CtrlSize', 'CtrlStyle')
    
    def __init__(self, validator, title="Data", ctrlSize=None, ctrlStyle=0, msg=None): 
        """
        validator : Validator object (cer.value.validator)
        title     : Dialog Title
        ctrlSize  : Size for DataCtrl
        ctrlStyle : Style for DataCtrl
        msg       : Message to display. Default to title
        """
        self._cerval = validator
        self.Title = title
        self.Msg = msg
        self.CtrlSize = ctrlSize
        self.CtrlStyle = ctrlStyle
    
    def GetText(self, value):
        return self._cerval.getText(value)
    
    def __call__(self, parent, value=None):
        dlg = DataDialog(parent, self._cerval, self.Title, value, self.CtrlSize,
                         self.CtrlStyle,  self.Msg)
        value = dlg.Data if dlg.ShowModal() == wx.ID_OK else None
        dlg.Destroy()
        return value

#-----------------------------------------------------------------------------------------

"""
def get_text(parent, title="Text", value=None, format="%s", msg=None,
             ctrlSize=None, ctrlStyle=0):
    #Presenta diálgo y retorna string ingresado o None
    val = TextValidator(format)
    getter = DataGetter(val, title, msg, ctrlSize, ctrlStyle)
    return getter(parent, value)

def get_int(parent, title="Int", value=None, format="%d", vmin=None, vmax=None,
            msg=None, ctrlSize=None, ctrlStyle=0):
    #Presenta diálgo y retorna int ingresado o None
    val = IntValidator(format, vmin, vmax)
    getter = DataGetter(val, title, msg, ctrlSize, ctrlStyle)
    return getter(parent, value)

def get_float(parent, title="Float", value=None, format="%.2f", vmin=None, vmax=None,
            msg=None, ctrlSize=None, ctrlStyle=0):
    #Presenta diálgo y retorna float ingresado o None
    val = FloatValidator(format, vmin, vmax)
    getter = DataGetter(val, title, msg, ctrlSize, ctrlStyle)
    return getter(parent, value)

def get_datetime(parent, title="DateTime", value=None, format="%d/%m/%Y %H:%M", 
                 vmin=None, vmax=None, msg=None, ctrlSize=None, ctrlStyle=0):
    #Presenta diálgo y retorna datetime ingresado o None
    val = DateTimeValidator(format, vmin, vmax)
    getter = DataGetter(val, title, msg, ctrlSize, ctrlStyle)
    return getter(parent, value)
"""