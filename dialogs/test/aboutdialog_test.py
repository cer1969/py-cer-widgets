# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import wx
from cer.widgets import cw
from cer.widgets.resource.rxnuvola import resman

#-----------------------------------------------------------------------------------------

bigText  = u" Programa de prueba (R)"
longText = (u'\n\n'
            u' H.Q.I TRANSELEC CHILE S.A.\n'
            u' Administración Regional Coquimbo\n'
            u' Cristian Echeverría Rabí (R)\n'
            u' Versión experimental\n'
            u' En caso de problemas revisar archivo "errores.txt"\n'
            u' 29-08-2006')

#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.PySimpleApp(False)     # True para capturar stderr y stdout
    app.SetAssertMode(wx.PYAPP_ASSERT_EXCEPTION)
    
    cw.about(None, "Acerca de Test 2", bigText, longText, (400,300), 
             resman.Bitmap("cw_add_bookmark"))
    
    app.MainLoop()
