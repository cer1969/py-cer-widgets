# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ
# Archivo      : AboutDlgTest
# Fecha        : 29-08-2006 11:06:56 

import wx


app = wx.PySimpleApp(False)     # True para capturar stderr y stdout

clave = wx.GetPasswordFromUser("Ingrese clave")

if clave == "sofita":
    frame = wx.Frame(parent=None, title='Bare')
    frame.Center()
    frame.Show()
else:
    wx.MessageBox("Clave incorrecta","Error de acceso")

print wx.GetUserId()
app.MainLoop()