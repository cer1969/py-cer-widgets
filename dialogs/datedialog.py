# CRISTIAN ECHEVERRÍA RABÍ

import wx
import datetime

#-----------------------------------------------------------------------------------------

__all__ = ['format_date', 'GetDateDialog', 'DateGetter', 'get_date']

#-----------------------------------------------------------------------------------------
# Funciones utilitarias

def get_wxdate(myDate):
    """Retorna wx.DateTime object
    myDate: datetime.date object.
    """
    return wx.DateTime.FromDMY(myDate.day,myDate.month-1,myDate.year)

def get_pydate(myDate):
    """Retorna datetime.date object
    myDate: wx.DateTime object.
    """
    return datetime.date(myDate.GetYear(),myDate.GetMonth()+1,myDate.GetDay())

def format_date(myDate, format="%d/%m/%Y"):
    """Formatea datetime.date
    myDate: datetime.date object.
    format: string de formato para strftime.
    """
    return myDate.strftime(format)

#-----------------------------------------------------------------------------------------

class GetDateDialog(wx.Dialog):
    """Cuadro de diálogo para ingreso de fechas"""
    
    def __init__(self, parent, title="Date", value=None, vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=None, msg=None
                 ):
        """
        """ 
        
        wx.Dialog.__init__(self, parent, -1, title)
        
        self.Value = None
        
        _vmin = datetime.date.min if vmin is None else vmin
        _vmax = datetime.date.max if vmax is None else vmax
        _size = (150, -1) if ctrlSize is None else ctrlSize
        _style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY if ctrlStyle is None else ctrlStyle
        _msg = title if msg is None else msg
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        st = wx.StaticText(self, -1, _msg)
        box.Add(st, 0, wx.EXPAND|wx.ALL, 10)
        
        _value = datetime.date.today() if (value is None) else value
        _date = get_wxdate(_value)
        self.ctrl = wx.adv.DatePickerCtrl(self, -1, _date, size=_size, style=_style)
        self.ctrl.SetRange(get_wxdate(_vmin), get_wxdate(_vmax))
        box.Add(self.ctrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        okbut = wx.Button(self, wx.ID_OK, "Ok")
        okbut.SetDefault()
        oksizer.Add(okbut, 0, wx.RIGHT, 10)
        oksizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"),0 , wx.ALL, 0)
        box.Add(oksizer,0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        box.Fit(self)
        box.SetSizeHints(self)
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        
        self.CentreOnParent(wx.BOTH)
    
    def OnOk(self,event=None):
        self.Value = get_pydate(self.ctrl.GetValue())
        self.EndModal(wx.ID_OK)

    def OnCancel(self,event=None):
        self.EndModal(wx.ID_CANCEL)

#-----------------------------------------------------------------------------------------

class DateGetter(object):
    """Callable: Presenta GetDateDialog y retorna valor"""
    
    __slots__ = ('Title', 'Format', 'Vmin', 'Vmax', 'CtrlSize', 'CtrlStyle', 'Msg')
    
    def __init__(self, title="Date", format=None, vmin=None, vmax=None, ctrlSize=None,
                 ctrlStyle=None, msg=None
                 ):
        """ 
        """
        self.Title = title
        self.Format = "%d/%m/%Y" if format is None else format
        self.Vmin = vmin
        self.Vmax = vmax
        self.CtrlSize = ctrlSize
        self.CtrlStyle = ctrlStyle
        self.Msg = msg

    def GetText(self, value):
        if value is None:
            return ""
        return format_date(value, self.Format)
    
    def __call__(self, parent, value=None):
        dlg = GetDateDialog(parent, self.Title, value, self.Vmin, self.Vmax,
                            self.CtrlSize, self.CtrlStyle, self.Msg)
        value = dlg.Value if dlg.ShowModal() == wx.ID_OK else None
        dlg.Destroy()
        return value

#-----------------------------------------------------------------------------------------

def get_date(parent, title="Date", value=None, vmin=None, vmax=None, ctrlSize=None, 
             ctrlStyle=None, msg=None
             ):
    """Presenta diálgo y retorna datetime.date seleccionado o None"""
    getter = DateGetter(title, None, vmin, vmax, ctrlSize, ctrlStyle, msg)
    return getter(parent, value)