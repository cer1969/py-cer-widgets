# CRISTIAN ECHEVERRÍA RABÍ 

import wx
from cer.widgets import cw
import wx.grid as gridlib
import cer.widgets.grid as grid
from cer.widgets.resource.rxnuvola import resman

#-----------------------------------------------------------------------------------------
# Definición de Commands

cmd = cw.CommandList()
cmd_addr = cmd.Item("Add Row", "AddRow", "cw_tb_addrow")
cmd_insr = cmd.Item("Ins Row", "InsRow", "cw_tb_insrow")
cmd_test = cmd.Item("Test Data", "TestData")
cmd_rep = cmd.Item("Reemplazar", "ReplaceData")
cmd_delr = cmd.Item("Del Row", "DelRow", "cw_tb_delrow")
cmd_past = cmd.Item("Paste Data", "PasteData", "cw_tb_pasterows")
cmd_lins = cmd.Item("Agrega Datos", "AddData", "cw_file_open")

mbd = cw.MenuBar(
    cw.Menu("&Archivo", cmd_addr, cmd_insr, cmd_test, cmd_rep)
)

tbd = cw.ToolBar(None, None, cmd_addr, cmd_insr, cmd_delr, cmd_past, cmd_lins)

#-----------------------------------------------------------------------------------------
# Definición del DataModel para usar con el grid

dam = grid.TableDataModel(
    grid.Text(u"Nombre", u"Nuevo"),
    grid.Int("Edad", 34),
    grid.Float("Peso", 75.5),
    grid.Choice(u"Profesión\nActual", u"Médico", args=u"Ingeniero,Abogado,Agricultor,Médico,Constructor"),
    grid.Bool("Contratado",1)
)
dat = [["Cristian",x,75,"Agricultor",True] for x in range(5)]
datx = [["Mono",x,50,"Chile",False] for x in range(10)]
dam.Data = dat

#-----------------------------------------------------------------------------------------

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Text CerSimpleGrid", size=(400,400))

        self.SetMenuBar(mbd.Make())
        self.SetToolBar(tbd.Make(self))
        self.CreateStatusBar(1)

        self.p = grid.Grid(self, dam)
        self.p.AutoAddRows = True
        self.p.EnterMove = grid.ENTER_MOVE_NEXTEDIT
        self.p.SetRowLabelWidthInChars(5)
        self.p.SetColLabelHeightInChars(2, 4)
        self.p.SetGridCursor(0, 1) 
        
        self.p.AutoSizeColumns(False) # Fija ancho columna, pero no establece el mínimo
        #self.p.AutoSizeRows(False) # Fija alto fila, pero no establece el mínimo
        
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour(wx.Colour(255, 255, 238))
        attr.SetReadOnly(True)
        self.p.SetColAttr(0, attr)
        
        attr2 = gridlib.GridCellAttr()
        attr2.SetTextColour("RED")
        attr2.SetReadOnly(False)
        self.p.SetColAttr(2, attr2)
        self.p.SetColFormatFloat(2, -1, 2)
        
        cmd.Bind(self)
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    
    def OnSize(self, event):
        self.p.AdjustScrollbars()
        event.Skip()
    
    def AddRow(self, event):
        self.p.AppendRows()
    
    def InsRow(self, event):
        self.p.InsertSelectedRows()
    
    def DelRow(self, event):
        self.p.DeleteSelectedRows()
    
    def ReplaceData(self, event):
        self.p.ReplaceData(datx)
    
    def PasteData(self, event):
        data = [["A", 1, 1, "Ingeniero", 1],
                ["B", 2, 2, "Ingeniero", 0],
                ["C", 3, 3, "Ingeniero", 0]]
        self.p.InsertRowsData(1, data)
    
    def AddData(self, event):
        data = [["A", 1, 1, "Ingeniero", 0],
                ["B", 2, 2, "Ingeniero", 1],
                ["C", 3, 3, "Abogado",   1]]
        for i in data:
            self.p.DataModel.Data.append(i)
        self.p.UpdateRowsView()
        #self.p.AppendRowsData(data)
    
    def TestData(self, event):
        datamodel = self.p.DataModel
        sal = []
        for row in range(datamodel.GetNumberRows()):
            r = []
            for col in range(datamodel.GetNumberCols()):
                r.append(datamodel.GetValue(row, col))
            sal.append(r)
        for i in sal:
            print(i)

#-----------------------------------------------------------------------------------------
# Test code

if __name__ == '__main__':
    
    from wx.lib import colourdb
    
    app = wx.App(False)     # True para capturar stderr y stdout
    app.resman = resman
    
    colourdb.updateColourDB()
    app.SetAssertMode(wx.APP_ASSERT_DIALOG)
    MainFrame().Show(True)
    app.MainLoop()