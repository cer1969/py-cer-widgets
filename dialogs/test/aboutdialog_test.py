# CRISTIAN ECHEVERRÍA RABÍ 

import wx
from cer.widgets import cw
from cer.widgets.resource.rxnuvola import resman

#-----------------------------------------------------------------------------------------

bigText  = " Programa de prueba (R)"
longText = ('\n\n'
            ' H.Q.I TRANSELEC CHILE S.A.\n'
            ' Administración Regional Coquimbo\n'
            ' Cristian Echeverría Rabí (R)\n'
            ' Versión experimental\n'
            ' En caso de problemas revisar archivo "errores.txt"\n'
            ' 29-08-2006')

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.APP_ASSERT_EXCEPTION)
    
    cw.about(None, "Acerca de Test 2", bigText, longText, (400,300), resman.Bitmap("cw_add_bookmark"))
    
    app.MainLoop()
