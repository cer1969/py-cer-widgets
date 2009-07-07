# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ
# Archivo      : ClipboardTest
# Fecha        : 29-08-2006 11:44:36 

from cer.gui import cg
import wx

#-----------------------------------------------------------------------------------------

if not wx.GetApp():
    app = wx.PySimpleApp()
print cg.Clipboard.GetFloatTable(repList=[(".",""),(",",".")])
print "Hola"
