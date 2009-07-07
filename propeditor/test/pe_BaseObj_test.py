# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import wx
from cer.widgets import cw
import cer.widgets.propeditor as pe
import datetime

#-----------------------------------------------------------------------------------------

data1 = pe.EditorData(
    pe.Text("nombre", msg="Nombre completo"),
    pe.Text("empresa", msg=u"Razón social de la empresa"),
    pe.EditorGroup("Medidas", u"Características físicas generales",
        pe.Float("altura", format="%.3f", msg="Altura del empleado en metros"),
        pe.Float("peso", "Peso", msg="Peso del empleado en kilos"),
        pe.Int("edad", vmin=30, vmax=90, msg=u"Edad en años")
    ),
    pe.Text("mensaje", ctrlSize=(250,130), ctrlStyle=wx.TE_MULTILINE, msg=u"Mensaje corto"),
    pe.DateTime("feh", "Fecha y Hora")
)

obj1 = data1.CreateObj()
obj1.nombre = "Cristian"
obj1.empresa = "Transelec"
obj1.altura = 1.7
obj1.edad = 35
obj1.mensaje = "-"

#-----------------------------------------------------------------------------------------

class Persona:
    def __init__(self, name):
        self.Name = name

personas = [Persona(x) for x in ["Pedro", "Juan", "Diego", "Lucas"]]


data2 = pe.EditorData(
    pe.EditorGroup("Fecha", u"Dato de pruba",
        pe.Time("inicio", format="%H:%M:%S", vmin=datetime.time(8,30,0),
                vmax=datetime.time(18,00,0), useSecs=True,
                msg=u"Ingrese hora de inicio (horario hábil 8:30 - 18:00)")
    ),
    pe.EditorGroup("Otros", u"Otros datos",
        pe.Date("fnac", "Fecha Nacimiento", msg="Fecha de nacimiento empleado"),
        pe.Switch("cocina", ["Si","No","Mas o menos"], msg="Habilidades culinarias"),
        pe.Float("peso", "Peso", edit=False, msg="Peso del empleado en kilos"),
        pe.Choice("actividad", ["Cantar","Futbol","Tenis","Voleiball","Otras"],
                  msg="Actividad Extra-programatica")
    ),
    pe.Choice("persona", personas, getText=cw.GetTextAttrFunc("Name"), 
              msg="Selecione objeto")
)

obj2 = data2.CreateObj()
obj2.inicio = datetime.time(13,20,15)
obj2.peso = 74
obj2.actividad = "Tenis"
obj2.persona = personas[2]


#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Editor with BaseObj", size=(500,600))
        
        p = wx.Panel(self,-1)
        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = cw.TipBox(p, size=(-1,100), showValue=True)
        
        plc1 = pe.Editor(p, data1, obj1, (150, 130, 0), style=pe.PREDIT_DEF_STYLE|wx.TR_TWIST_BUTTONS)
        plc1.MsgBox = txt
        
        plc2 = pe.Editor(p, data2, None, (150, 130, 50))
        plc2.MsgBox = txt
        
        box.Add(plc1, 1, wx.EXPAND|wx.ALL, 5)
        box.Add(plc2, 1, wx.EXPAND|wx.ALL, 5)
        box.Add(txt,  0, wx.EXPAND|wx.ALL, 5)
        
        p.SetAutoLayout(True)
        p.SetSizer(box)
        box.Fit(p)

        #self.Fit()
        
        plc1.Bind(pe.EVTC_PREDIT_VALCHANGE, self.Test)#, id=pe1.GetId())
        plc2.Bind(pe.EVTC_PREDIT_VALCHANGE, self.Test)#, id=pe1.GetId())
        
        self.Center(wx.BOTH)
    
    def Test(self, event):
        ctrl = event.Ctrl
        name = event.Item.Name
        print "Cambia valor de la propiedad %s" % name
        print ctrl.Obj.__dict__
        if name == "Peso":
            ctrl.SetEdit(ctrl.Data[2][1], False)
            #ctrl.SetEdit(ctrl.Data[2], False)
            print ctrl.Data[2][1].Edit
            ctrl.UpdateFormats()

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    from wx.lib import colourdb

    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
    colourdb.updateColourDB()
    MainFrame().Show(True)
    app.MainLoop()