# CRISTIAN ECHEVERRÍA RABÍ 

import wx
from cer.widgets import cw

#-----------------------------------------------------------------------------------------
# Definición de comandos

cmd = cw.CommandList()
cmd_new   = cmd.Item("&Nuevo...\tAlt-N", "Test", "cw_new", "Crear nuevo archivo")
cmd_open  = cmd.Item("&Abrir...\tAlt-A", "Test", "cw_file_open")
cmd_save  = cmd.Item("&Grabar\tAlt-G", "Test", "cw_file_save", "Grabar archivo")
cmd_savas = cmd.Item("Grabar como...", "Test", "cw_file_save_as")

cmd_hdtb2 = cmd.Item("Oculta ToolBar2\tAlt-H", "HideTool2")
cmd_swtb2 = cmd.Item("Muestra ToolBar2\tAlt-S", "ShowTool2")

cmd_exit  = cmd.Item("&Salir", "OnCloseWindow", "cw_quit", "Fin aplicación")

cmd_check = cmd.Check("Check", "Test", "cw_tip", bmp2="cw_file_save")
cmd_rad01 = cmd.Radio("Opcion1", "Test")
cmd_rad02 = cmd.Radio("Opcion2", "Test")
cmd_rad03 = cmd.Radio("Opcion3", "Test")

_subm = cw.Menu("Loco", cmd_check, None, cmd_rad01, cmd_rad02, cmd_rad03)
cmd_subm  = cmd.Sub(_subm, "cw_new")

cmd_tabla = cmd.Check("Tabla", "Test", "cw_tb_tabla", args=100)
cmd_tabar = cmd.Check("Agrega Filas", "Test", "cw_tb_addrow", args=200)
cmd_tabdr = cmd.Check("Elimina filas", "Test", "cw_tb_delrow", args=300)
cmd_tabl2 = cmd.Radio("Tabla", "Test", "cw_tb_tabla", args=1)
cmd_taba2 = cmd.Radio("Agrega Filas", "Test", "cw_tb_addrow", args=2)
cmd_tabd2 = cmd.Radio("Elimina filas", "Test", "cw_tb_delrow", args=3)

#-----------------------------------------------------------------------------------------
# Creación barra de menú de aplicación

mbd = cw.MenuBar(
    cw.Menu("&Archivo", 
            cmd_new, cmd_open, cmd_save, cmd_savas, None,
            cmd_hdtb2, cmd_swtb2, None,
            cmd_exit
    ),
    cw.Menu("Test",
            cmd_rad01,cmd_rad02,cmd_rad03),
    cw.Menu("Ayuda",
            #cmd_subm, cmd_hdtb2, cmd_swtb2, cmd_exit)  # NO FUNCIONA SUBMENU
            cmd_hdtb2, cmd_swtb2, cmd_exit)
)

#-----------------------------------------------------------------------------------------

# Creación ToolBar de aplicación
tbd = cw.ToolBar(None, (16, 16), 
    cmd_new, cmd_open, cmd_save, None, cmd_tabla, cmd_tabar, cmd_tabdr
)

# Creación ToolBar2 de aplicación
tbd2 = cw.ToolBar(wx.TB_VERTICAL, (16, 16),
    cmd_tabl2, cmd_taba2, cmd_tabd2
)

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    print(cmd)
    c = tbd.GetTool(cmd_tabla.Id)
    print(c.Args)
    print(cw.CMD_ITEM, cw.CMD_CHECK, cw.CMD_RADIO, cw.CMD_SUB)
