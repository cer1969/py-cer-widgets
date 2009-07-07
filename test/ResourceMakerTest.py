# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ
# Archivo      : ResourceMakerTest
# Fecha        : 29-08-2006 10:59:05 

import wx
from cer.widgets.resource.resourcemaker import ResourceMaker,RESWX

#-----------------------------------------------------------------------------------------
crm = ResourceMaker()
crm.UpdateAll(RESWX)

#crm.AddImageList("toolbar1",16,16,("NEW","FILE_OPEN","FILE_SAVE"))


crm.AddString("loco",u"Cristian Echeverría")
crm.AddStringPyFile("string.data")
crm.AddStringFile("string.data",True)
#crm.AddStringDir(r"C:\CER\000Devel\WinPerfil\test")

crm.AddFont("tahoma08b",wx.Font( 8,wx.SWISS,wx.NORMAL,wx.BOLD,False,"Tahoma"))

crm.Make("myres.py")
