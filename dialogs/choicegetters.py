# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx, string

#-----------------------------------------------------------------------------------------

__all__ = ['GetTextFunc', 'GetTextAttrFunc', 'SwitchGetter', 'ChoiceGetter', 'get_choice']

#-----------------------------------------------------------------------------------------

class GetTextFunc(object):
    """Callable: Formatea valor a string"""
    
    __slots__ = ('Format',)
    
    def __init__(self, format="%s"):
        self.Format = format
    
    def __call__(self, value):
        if value is None:
            return ""
        return self.Format % value

#-----------------------------------------------------------------------------------------

class GetTextAttrFunc(object):
    """
    Callable: Formatea attributo de objeto
    Permite pasar una lista de objetos al ChoiceGetter y a get_choice
    """
    
    __slots__ = ('Attr', 'Format',)
    
    def __init__(self, attr, format="%s"):
        self.Attr = attr
        self.Format = format
    
    def __call__(self, obj):
        if obj is None:
            return ""
        return self.Format % getattr(obj, self.Attr)

#-----------------------------------------------------------------------------------------

class SwitchGetter(object):
    """Callable: Getter para hacer switch entre valores. No despliega dialog"""
    
    __slots__ = ('Choices', 'GetText')
    
    def __init__(self, choices, getText=None):
        """
        choices: Lista con valores para iterar.
        getText: Función para formatear presentación de valor seleccionado.
        
        """
        self.Choices = choices
        self.GetText = GetTextFunc() if getText is None else getText
    
    def __call__(self, parent, value=None):
        _idx = 0 if (value is None) else (self.Choices.index(value) + 1)
        if _idx >= len(self.Choices):
            _idx = 0
        return self.Choices[_idx]

#-----------------------------------------------------------------------------------------

class ChoiceGetter(object):
    """Callable: Presenta wx.SingleChoiceDialog y retorna valor"""
    
    __slots__ = ('Choices', 'Title', 'GetText', '_txtchoices', 'Msg')
    
    def __init__(self, choices, title="Choice", getText=None, msg=None):
        """
        """
        _getText = GetTextFunc() if getText is None else getText
        self._txtchoices = [_getText(x) for x in choices]
        
        self.Choices = choices
        self.Title = title
        self.GetText = _getText
        self.Msg = title if msg is None else msg

    def __call__(self, parent, value=None):
        dlg = wx.SingleChoiceDialog(parent, self.Msg, self.Title, self._txtchoices)
        
        _sel = 0 if value is None else self.Choices.index(value)
        dlg.SetSelection(_sel)
        
        op = dlg.ShowModal()
        _sel = dlg.GetSelection()
        dlg.Destroy()
        if op == wx.ID_OK:
            return self.Choices[_sel]
        return None

#-----------------------------------------------------------------------------------------
 
def get_choice(parent, choices, title="Choice", value=None, getText=None, msg=None):
    """Presenta diálgo y retorna selección o None"""
    getter = ChoiceGetter(choices, title, getText, msg)
    return getter(parent, value)