# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Menu','MenuBar']

#-----------------------------------------------------------------------------------------

class Menu(list):
    """Maneja datos de items y crea wx.Menu"""

    __slots__ = ('Title',)

    def __init__(self, title, *items):
        """
        title: Título del menú
        items: Lista de cw.Command con ítems del menú
        """
        list.__init__(self, items)
        self.Title = title
    
    def Make(self):
        """Retorna wx.Menu"""
        m = wx.Menu()
        for item in self:
            if item is None:
                m.AppendItem(wx.MenuItem(m, wx.ID_SEPARATOR))
            else:
                mi = item.CreateMenu(m)
                m.AppendItem(mi)
        return m

#-----------------------------------------------------------------------------------------

class MenuBar(list):
    """Maneja datos de items y crea wx.MenuBar"""
    
    __slots__ = ()
    
    def __init__(self, *menus):
        """
        menus: Lista de cw.Menu
        """
        list.__init__(self, menus)
    
    def Make(self):
        """Retorna wx.MenuBar"""
        mb = wx.MenuBar()
        for menu in self:
            m = menu.Make()
            mb.Append(m, menu.Title)
        return mb