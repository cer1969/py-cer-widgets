# CRISTIAN ECHEVERRÍA RABÍ 

import wx
from cer.widgets import cw

#-----------------------------------------------------------------------------------------

def show(value):
    if value is None:
        print ("-- CANCELADO --")
    elif type(value) is str:
        print (value.encode("Latin-1"))
    else:
        print (value)

#-----------------------------------------------------------------------------------------

app = wx.App(False)     # True para capturar stderr y stdout


mt = cw.get_time(None, "Tiempo", useSecs=True, msg="Ingrese hora")
show(mt)

value = cw.get_choice(None, [1,2,3,4], "Choice Test", msg="Selecciona")
if value:
    print (value + 100)

date = cw.get_date(None, "Test Date", msg="Fecha de Nacimiento")
show(date)

mydt = cw.get_datetime(None,"Test DateTime", useSecs=True, msg="Fecha y hora")
show(mydt)