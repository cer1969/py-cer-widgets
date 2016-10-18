# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['CMD_ITEM','CMD_CHECK','CMD_RADIO','CMD_SUB','Command','CommandList']

#-----------------------------------------------------------------------------------------

def _get_resman():
    # Función de transición para obtener resman
    # Las aplicaciones que usan cer.application definen resman en cerapp.resman
    # Las otras aplicaciones definen resman en wx.GetApp().resman
    try:
        # Verifica si está definido en cerapp
        return cerapp.resman
    except NameError:
        try:
            # Verifica si está definido en wx.GetApp()
            return wx.GetApp().resman
        except AttributeError:
            return None

#-----------------------------------------------------------------------------------------
# Constantes para diferenciación de tipos de items

CMD_ITEM      = wx.ITEM_NORMAL
CMD_CHECK     = wx.ITEM_CHECK
CMD_RADIO     = wx.ITEM_RADIO
CMD_SUB       = 1000

#-----------------------------------------------------------------------------------------

class Command(object):
    """Clase para comandos de Menú y Toolbar"""
    
    __slots__ = ('Text','Method','Bmp','Help','Bmp2','Args','Type','Sub','Id')
    

    def __init__(self, text="", method="", bmp="", help="", bmp2="", args=None, 
                 type=CMD_ITEM, sub=None):
        """
        text: String. Texto del menú o tooltip
        method: String. Nombre del metodo asociado al comando
        bmp: String. Nombre de imagen asociada al comando
        help: String. Texto de ayuda en barra de estado
        bmp2: String. Nombre de imagen alternativa
        args: Otros argumentos del Command
        type: tipo de Command
        sub: Objeto wx.Menu
        
        """
        self.Text = text
        self.Method = method
        self.Bmp = bmp
        self.Help = help
        self.Bmp2 = bmp2
        self.Args = args
        self.Type = type
        self.Sub = sub
        self.Id = wx.NewId()
    
    def CreateMenu(self, menu):
        if self.Type == CMD_SUB:
            m = self.Sub.Make()
            mi = wx.MenuItem(menu, -1, self.Sub.Title, subMenu=m)
        else:
            mi = wx.MenuItem(menu, self.Id, self.Text, self.Help, self.Type)
        
        resman = _get_resman()
        if resman and (self.Bmp != ""):
            bmp  = resman.Bitmap(self.Bmp)
            if self.Bmp2 != "":
                bmp2 = resman.Bitmap(self.Bmp2)
                mi.SetBitmaps(bmp, bmp2)
            else:
                mi.SetBitmap(bmp)
        return mi
    
    def CreateTool(self, tb):
        if self.Type != CMD_SUB:
            resman = _get_resman()
            im = resman.Bitmap(self.Bmp)
            if self.Type == CMD_CHECK:
                tb.AddCheckTool(self.Id, im, shortHelp=self.Text, longHelp=self.Help)
            elif self.Type == CMD_RADIO:
                tb.AddRadioTool(self.Id, im, shortHelp=self.Text, longHelp=self.Help)
            else:
                tb.AddLabelTool(self.Id, self.Text, im, shortHelp=self.Text, 
                                longHelp=self.Help)

#-----------------------------------------------------------------------------------------

class CommandList(list):
    
    def _cmd(self, text, method, bmp="", help="", bmp2="", args = None, type=CMD_ITEM):
        cmd = Command(text, method, bmp, help, bmp2, args, type)
        self.append(cmd)
        return cmd
    
    def Item(self, text, method, bmp="", help="", bmp2="", args = None):
        return self._cmd(text, method, bmp, help, bmp2, args, CMD_ITEM)
    
    def Check(self, text, method, bmp="", help="", bmp2="", args = None):
        return self._cmd(text, method, bmp, help, bmp2, args, CMD_CHECK)
    
    def Radio(self, text, method, bmp="", help="", bmp2="", args = None):
        return self._cmd(text, method, bmp, help, bmp2, args, CMD_RADIO)
    
    def Sub(self, sub, bmp="", help=""):
        cmd = Command("", bmp=bmp, help=help, type=CMD_SUB, sub=sub)
        return cmd
    
    def Bind(self, parent, methodOwner=None):
        # Se verifica si el methodOwner es distinto al parent
        if not methodOwner:
            methodOwner = parent
        for tool in self:
            parent.Bind(wx.EVT_MENU, getattr(methodOwner, tool.Method), id=tool.Id)
