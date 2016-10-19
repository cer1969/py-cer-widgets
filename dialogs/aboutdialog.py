# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['AboutDialog','about']

#-----------------------------------------------------------------------------------------

_INFO_STYLE = wx.TE_READONLY|wx.TE_RICH2|wx.TE_LEFT| wx.TE_MULTILINE|wx.STATIC_BORDER

class AboutDialog(wx.Dialog):
    """Clase AboutDialog"""
    
    def __init__(self, parent, title="Acerca de...", infoSize=(300,200), bmp=None):
        """
        title: Título del diálogo.
        infoSize: Dimensiones del área de texto.
        bmp: Bitmap para la parte superior del diálogo.
        
        """
        wx.Dialog.__init__(self,parent,-1,title)

        box = wx.BoxSizer(wx.VERTICAL)

        if bmp:
            sbmp = wx.StaticBitmap(self, -1, bmp)
            box.Add(sbmp,0,wx.CENTER|wx.TOP|wx.LEFT|wx.RIGHT,10)

        self._info = wx.TextCtrl(self, -1, "", size=infoSize, style=_INFO_STYLE)
        
        _fgColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
        _bgColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        
        self._info.SetBackgroundColour(_bgColour)
        self._info.SetForegroundColour(_fgColour)
        
        _lf = self._info.GetFont()
        _bf = wx.Font(_lf.GetPointSize()+3, _lf.GetFamily(), _lf.GetStyle(), wx.FONTWEIGHT_BOLD)
        
        self.LongTextAttr = wx.TextAttr(_fgColour, _bgColour, _lf)
        self.BigTextAttr = wx.TextAttr(_fgColour, _bgColour, _bf)

        box.Add(self._info,1,wx.EXPAND|wx.ALL,10)

        okBut = wx.Button(self,wx.ID_OK,"Ok")
        okBut.SetDefault()
        box.Add(okBut,0,wx.CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        #wx.EVT_BUTTON(self,wx.ID_OK,self.OnOk)
        #wx.EVT_BUTTON(self,wx.ID_CANCEL,self.OnCancel)

        self.SetSizer(box)
        box.SetSizeHints(self)
        self.Layout()

        self.CentreOnParent(wx.BOTH)

    def SetText(self, bigText=" Programa (R)", longText=""):
        self._info.Clear()
        self._info.SetDefaultStyle(self.BigTextAttr)
        self._info.WriteText(bigText)
        self._info.SetDefaultStyle(self.LongTextAttr)
        self._info.WriteText(longText)
        
    def OnCancel(self,event=None):
        self.EndModal(wx.ID_CANCEL)

    def OnOk(self,event=None):
        self.EndModal(wx.ID_OK)

#-----------------------------------------------------------------------------------------

def about(parent, title="Acerca de...", bigText=" Nombre del Programa (R)", longText="", 
          infoSize=(300,200), bmp=None):
    """Funtion About: Despliega AboutDialog
    parent: Ventana padre. Puede ser None.
    title: Título del diálogo.
    bigText: Texto destacado en área de texto. Normalmente para uso de encabezado.
    longText: Texto normal de área de texto. Normalemte es un texto largo con detalles.
    infoSize: Dimensiones del área de texto.
    bmp: Bitmap para la parte superior del diálogo.
    """
    dlg = AboutDialog(parent, title, infoSize, bmp)
    dlg.SetText(bigText, longText)
    dlg.ShowModal()
    dlg.Destroy()