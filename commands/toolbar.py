# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['ToolBar']

#-----------------------------------------------------------------------------------------

class ToolBar(list):
    """Almacena items y crea wx.ToolBar"""
    
    __slots__ = ('Style','Size')

    def __init__(self, style, size, *tools):
        """
        style: Estilo del ToolBar
        size: Size imágenes del ToolBar
        tools: Lista de objetos cw.Command
        """
        list.__init__(self, tools)
        self.Style = wx.TB_FLAT|wx.TB_HORIZONTAL if style is None else style
        self.Size = (16, 16)if size is None else size
        
    #-------------------------------------------------------------------------------------
    
    def GetTool(self, id_):
        """Devuelve objeto cw.Command
        id_ : Id del objeto buscado.
        """
        sal = [x for x in self if x <> None]
        sal = [x for x in sal if x.Id==id_]
        return sal[0]
    
    #-------------------------------------------------------------------------------------
    
    def Make(self, parent):
        """Retorna wx.ToolBar"""
        tb = wx.ToolBar(parent, -1, style=self.Style)
        tb.SetToolBitmapSize(self.Size)
        for tool in self:
            if tool is None:
                tb.AddSeparator()
            else:
                tool.CreateTool(tb)
        tb.Realize()
        return tb