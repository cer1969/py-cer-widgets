# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Text', 'Number', 'DateTime']

#-----------------------------------------------------------------------------------------

class Text(object):
    
    __slots__ = ('_text', '_width', '_align', 'format', 'attr', 'pos', 'ctrl')
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_LEFT,
                 format="%s", attr=None):
        
        self._text = text
        self._width = width
        self._align = align
        self.format = format
        self.attr = attr
        self.pos = None
        self.ctrl = None
    
    def insert(self, pos, ctrl):
        self.pos = pos
        self.ctrl = ctrl
        ctrl.InsertColumn(pos, self._text, self._align, self._width)
    
    #-------------------------------------------------------------------------------------
    # Propiedad text
    
    def _getText(self):
        return self._text
    
    def _setText(self, value):
        self._text = value 
        pos = self.pos
        col = self.ctrl.GetColumn(pos)
        col.SetText(value)
        self.ctrl.SetColumn(pos, col)
    
    text = property(_getText, _setText)
    
    #-------------------------------------------------------------------------------------
    # Propiedad width
    
    def _getWidth(self):
        return self._width
    
    def _setWidth(self, value):
        self._width = value
        pos = self.pos
        self.ctrl.SetColumnWidth(pos, value)
    
    width = property(_getWidth, _setWidth)
    
    #-------------------------------------------------------------------------------------
    # Propiedad align
    
    def _getAlign(self):
        return self._align
    
    def _setAlign(self, value):
        self._align = value
        pos = self.pos
        col = self.ctrl.GetColumn(pos)
        col.SetAlign(value)
        self.ctrl.SetColumn(pos, col)
    
    align = property(wx.ListItem.GetAlign, _setAlign)
    
    #-------------------------------------------------------------------------------------
    def func(self, value):
        return self.format % value
    
    def toString(self, value):
        if value is None:
            return ""
        else:
            try:
                return self.func(value)
            except TypeError as _e:
                return ">> Error"

#-----------------------------------------------------------------------------------------

class Number(Text):
    
    __slots__ = ()
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_RIGHT,
                 format="%d", attr=None):
        Text.__init__(self, text, width, align, format, attr)


#-----------------------------------------------------------------------------------------

class DateTime(Text):
    
    __slots__ = ()
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_RIGHT,
                 format="%d/%m/%y - %H:%M", attr=None):
        Text.__init__(self, text, width, align, format, attr)
    
    def func(self, value):
        return value.strftime(self.format)