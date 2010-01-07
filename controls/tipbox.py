# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['TipBox']

#-----------------------------------------------------------------------------------------

class TipBox(wx.TextCtrl):
    """Control de texto que muestra texto de ayuda.
    Utilitario para otras clases como PropertyList.
    
    """
    def __init__(self, parent, size=(-1,50), showValue=True, style=0):
        """
        size: Tamaño del TextCtrl.
        showValue: True para mostrar value (tercer argumento de SetText. Default True.
        style: Estilo del TextCtrl.
        
        """
        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.STATIC_BORDER|style
        wx.TextCtrl.__init__(self, parent, -1, "", size=size, style=style)
        
        self.showValue = showValue
        
        _fgColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
        _bgColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        
        self.SetForegroundColour(_fgColour)
        self.SetBackgroundColour(_bgColour)
        
        _nf = self.GetFont()
        _bf = wx.Font(_nf.GetPointSize(), _nf.GetFamily(), _nf.GetStyle(), wx.FONTWEIGHT_BOLD)
        
        self.nameAttr = wx.TextAttr(_fgColour, _bgColour, _bf)
        self.textAttr = wx.TextAttr(_fgColour, _bgColour, _nf)
        self.valueAttr = wx.TextAttr("ROYALBLUE", "LIGHTYELLOW", _nf)
    
    def SetText(self, name, text, value=None):
        """Modifica texto del TextCtrl.
        name: Texto destacado
        test: Texto de detalle (en la misma línea que name.
        value: valor a presentar en línea siguiente.
        """
        self.SetValue("")
        self.SetDefaultStyle(self.nameAttr)
        self.WriteText(name + " : ")
        self.SetDefaultStyle(self.textAttr)
        self.WriteText(text)
        if (not self.showValue) or (value is None):
            return
        self.WriteText("\n")
        self.SetDefaultStyle(self.valueAttr)
        self.WriteText(value)