# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import wx
from cer.widgets import cw
import cer.widgets.propeditor as pe

#-----------------------------------------------------------------------------------------

class Cuenta(object):
    def __init__(self, banco, numero):
        self.banco = banco
        self.numero = numero

class Curso(object):
    def __init__(self, nombre, alumnos):
        self.nombre = nombre
        self.alumnos = alumnos

class Persona(object):
    def __init__(self, nombre, edad, peso, deporte):
        self.nombre = nombre
        self.edad = edad
        self.peso = peso
        self.deporte = deporte
        self.casado = 1
        self.cuenta = None
        self.curso = None

yo = Persona("Cristian", 38, 85, "Futbol")
yo.cuenta = Cuenta("Santander", 100200)
yo.curso = Curso("Matematica", 35)

curso2 = Curso("Historia", 25)
curso3 = Curso("Lenguaje", 6)

def getSiNo(value):
    if value == 1:
        return "Si"
    else:
        return "No"

#-----------------------------------------------------------------------------------------

data1 = pe.EditorData(
    pe.Text("nombre", msg="Nombre completo"),
    pe.Float("edad", msg=u"Edad en años"),
    pe.Float("peso", vmin=0, msg=u"Peso del empleado en kilos"),
    pe.Choice("deporte", ["Futbol","Tenis","Voleiball","Otras"], msg="Actividad Extra-programatica"),
    pe.EditorGroup("Cuenta Bancaria", u"Datos cuenta banco",
        pe.Text("cuenta.banco", u"Cuenta", msg=u"Nombre del Banco"),
        pe.Int("cuenta.numero", u"N°", msg=u"N° de cuenta")
    ),
    pe.EditorGroup("Curso", u"Ejemplo de como seleccionar de una lista de objetos\n y mostrar detalles",
        pe.Choice("curso", [yo.curso, curso2, curso3], "Nombre", getText=cw.GetTextAttrFunc("nombre"), msg="Selecione curso"),
        pe.Int("curso.alumnos", u"N° alumnos", msg=u"N° de alumnos", edit=False)
    ),
    pe.Switch("casado", [1,2], getText=getSiNo)
)

#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,"PropertyEditor Test", size=(500,600))
        
        p = wx.Panel(self,-1)
        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = cw.TipBox(p, size=(-1,100), showValue=True)
        
        plc1 = pe.Editor(p, data1, yo, colswidth=(150, 130, 0))#, style=cw.PREDIT_DEF_STYLE|wx.TR_TWIST_BUTTONS)
        plc1.MsgBox = txt
        
        box.Add(plc1, 1, wx.EXPAND|wx.ALL, 5)
        #box.Add(plc2, 1, wx.EXPAND|wx.ALL, 5)
        box.Add(txt,  0, wx.EXPAND|wx.ALL, 5)
        
        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)

        #self.Fit()
        
        plc1.Bind(pe.EVTC_PREDIT_VALCHANGE, self.Test)#, id=pe1.GetId())
        
        self.Center(wx.BOTH)
    
    def Test(self, event):
        ctrl = event.Ctrl
        ctrl.UpdateView()
        name = event.Item.Name
        print "Cambia valor de la propiedad %s" % name
        print ">>>>>", ctrl.Obj is yo
        obj = ctrl.Obj
        print (obj.nombre, obj.edad, obj.peso, obj.deporte)
        print (obj.cuenta.banco, obj.cuenta.numero, id(obj.cuenta))
        print (obj.curso.nombre, obj.curso.alumnos, id(obj.curso))
        print obj.casado

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()