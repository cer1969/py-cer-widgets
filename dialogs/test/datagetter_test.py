# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import wx
from cer.widgets import cw
import cer.utils.validators as cval

#-----------------------------------------------------------------------------------------

app = wx.App(False)     # True para capturar stderr y stdout

# Text -----------------

x = u"Juán"

val = cval.TextValidator()
print type(val.getText(x))
print type(val.getData("Pepe"))


getter = cw.DataGetter(val, "Ingrese Texto")
print getter(None, u"Cristian")
getter = cw.DataGetter(val, "Ingrese Texto largo", (250,150), wx.TE_MULTILINE)
print getter(None, u"Texto muy largo")

# Int ------------------
val = cval.IntValidator()
getter = cw.DataGetter(val, "Edad", msg="Ingrese entero")
print getter(None, 34)

val = cval.IntValidator(vmin=100, vmax=200)
getter = cw.DataGetter(val, "Rango Entero", msg="Ingrese entero entre 100 y 200")
print getter(None, 103)

# Float ----------------
val = cval.FloatValidator()
getter = cw.DataGetter(val, "Peso", msg="Ingrese float")
print getter(None, 84.4)

val = cval.FloatValidator("%.3f", vmin=-10, vmax=10)
getter = cw.DataGetter(val, "Rango Float", msg="Ingrese float entre -10 y 10")
print getter(None, 5)

val = cval.DateValidator()
getter = cw.DataGetter(val, "Fecha", msg="Ingrese fecha")
print getter(None, None)
