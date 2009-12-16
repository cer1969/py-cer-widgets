# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Text', 'Number', 'DateTime']

#-----------------------------------------------------------------------------------------

class Text(object):
    
    __slots__ = ('Name', 'Format', 'Width', 'Align', 'Attr')
    
    def __init__(self, name, width=wx.LIST_AUTOSIZE_USEHEADER, align=wx.LIST_FORMAT_LEFT,
                 format="%s", attr=None):
        self.Name   = name
        self.Width  = width
        self.Align  = align
        self.Format = format
        self.Attr   = attr
    
    def Func(self, value):
        return self.Format % value
    
    def GetText(self, value):
        if value is None:
            return ""
        else:
            try:
                return self.Func(value)
            except TypeError, _e:
                return ">> Error"

#-----------------------------------------------------------------------------------------

class Number(Text):
    
    __slots__ = ()
    
    def __init__(self, name, width=wx.LIST_AUTOSIZE_USEHEADER, align=wx.LIST_FORMAT_RIGHT,
                 format="%d", attr=None):
        Text.__init__(self, name, width, align, format, attr)


#-----------------------------------------------------------------------------------------

class DateTime(Text):
    
    __slots__ = ()
    
    def __init__(self, name, width=wx.LIST_AUTOSIZE_USEHEADER, align=wx.LIST_FORMAT_RIGHT,
                 format="%d/%m/%y - %H:%M", attr=None):
        Text.__init__(self, name, width, align, format, attr)
    
    def Func(self, value):
        return value.strftime(self.Format)