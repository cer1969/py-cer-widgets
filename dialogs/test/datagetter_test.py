# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import wx
from cer.widgets import cw
from cer.value import validator

#-----------------------------------------------------------------------------------------

app = wx.App(False)     # True para capturar stderr y stdout

# Text -----------------

x = u"Juán"

val = validator.Text()
print type(val.getText(x))
print type(val.getData("Pepe"))


getter = cw.DataGetter(val, "Ingrese Texto")
print getter(None, u"Cristian")
getter = cw.DataGetter(val, "Ingrese Texto largo", (250,150), wx.TE_MULTILINE)
print getter(None, u"Texto muy largo")

# Int ------------------
val = validator.Int()
getter = cw.DataGetter(val, "Edad", msg="Ingrese entero")
print getter(None, 34)

val = validator.Int(vmin=100, vmax=200)
getter = cw.DataGetter(val, "Rango Entero", msg="Ingrese entero entre 100 y 200")
print getter(None, 103)

# Float ----------------
val = validator.Float()
getter = cw.DataGetter(val, "Peso", msg="Ingrese float")
print getter(None, 84.4)

val = validator.Float("%.3f", vmin=-10, vmax=10)
getter = cw.DataGetter(val, "Rango Float", msg="Ingrese float entre -10 y 10")
print getter(None, 5)

val = validator.Date()
getter = cw.DataGetter(val, "Fecha", msg="Ingrese fecha")
print getter(None, None)
