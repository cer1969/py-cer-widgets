# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Text', 'Number', 'DateTime']

#-----------------------------------------------------------------------------------------

class Text(object):
    
    __slots__ = ('_typ', '_text', '_width', '_align', 'format', 'attr', 'pos', 'ctrl')
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_LEFT,
                 format="%s", attr=None):
        
        self._typ = "text"
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
    

    #-------------------------------------------------------------------------------------
    # Read-only properties

    @property
    def typ(self):
        return self._typ

    #-------------------------------------------------------------------------------------
    # Read-write properties
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value 
        pos = self.pos
        col = self.ctrl.GetColumn(pos)
        col.SetText(value)
        self.ctrl.SetColumn(pos, col)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        pos = self.pos
        self.ctrl.SetColumnWidth(pos, value)
    
    @property
    def align(self):
        return self._align
    
    @align.setter
    def align(self, value):
        self._align = value
        pos = self.pos
        col = self.ctrl.GetColumn(pos)
        col.SetAlign(value)
        self.ctrl.SetColumn(pos, col)


#-----------------------------------------------------------------------------------------

class Number(Text):
    
    __slots__ = ()
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_RIGHT,
                 format="%d", attr=None):
        Text.__init__(self, text, width, align, format, attr)
        self._typ = "number"


#-----------------------------------------------------------------------------------------

class DateTime(Text):
    
    __slots__ = ()
    
    def __init__(self, text, width=wx.LIST_AUTOSIZE, align=wx.LIST_FORMAT_RIGHT,
                 format="%d/%m/%y - %H:%M", attr=None):
        Text.__init__(self, text, width, align, format, attr)
        self._typ = "datetime"
    
    def func(self, value):
        return value.strftime(self.format)