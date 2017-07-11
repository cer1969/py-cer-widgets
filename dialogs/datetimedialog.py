# CRISTIAN ECHEVERRÍA RABÍ

import datetime
import wx, wx.adv
from .datedialog import get_wxdate, get_pydate
from .timedialog import _K_RANGE24, _K_RANGE60

CTRLDICT_DATE_DEF_STYLE = dict(size=(150,-1), style=wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)

#-----------------------------------------------------------------------------------------

__all__ = ['format_datetime', 'GetDateTimeDialog', 'DateTimeGetter', 'get_datetime']

#-----------------------------------------------------------------------------------------
# Funciones utilitarias

def format_datetime(myDate, format="%d/%m/%Y %H:%M"):
    """Formatea datetime.datetime
    myDate: datetime.datetime object.
    format: string de formato para strftime.
    """
    return myDate.strftime(format)

#-----------------------------------------------------------------------------------------

class GetDateTimeDialog(wx.Dialog):
    """Cuadro de diálogo para ingreso de fechas y horas"""

    def __init__(self, parent, title="DateTime", value=None, vmin=None, vmax=None, 
                 ctrlSize=None, ctrlStyle=None, useSecs=False, msg=None
                 ):
        """
        """ 
        wx.Dialog.__init__(self, parent, -1, title)
        
        self.Value = None
        _vmin = datetime.date.min if vmin is None else vmin
        _vmax = datetime.date.max if vmax is None else vmax
        _size = (150, -1) if ctrlSize is None else ctrlSize
        _style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY if ctrlStyle is None else ctrlStyle
        self.UseSecs = useSecs
        _msg = title if msg is None else msg
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        st = wx.StaticText(self, -1, _msg)
        box.Add(st, 0, wx.EXPAND|wx.ALL, 10)
        
        _value = datetime.datetime.now() if (value is None) else value
        
        # Date
        _date = get_wxdate(_value)
        self.ctrl = wx.adv.DatePickerCtrl(self, -1, _date, size=_size, style=_style)
        self.ctrl.SetRange(get_wxdate(_vmin), get_wxdate(_vmax))
        box.Add(self.ctrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        # Time
        self._h_ctrl = wx.Choice(self, choices=_K_RANGE24)
        self._m_ctrl = wx.Choice(self, choices=_K_RANGE60)
        
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self._h_ctrl, 1, wx.ALL, 0)
        box1.Add(wx.StaticText(self, -1, ":"), 0, 
                 wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        box1.Add(self._m_ctrl, 1, wx.ALL, 0)
        
        if useSecs:
            self._s_ctrl = wx.Choice(self, choices=_K_RANGE60)
            box1.Add(wx.StaticText(self, -1, ":"), 0, 
                     wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
            box1.Add(self._s_ctrl, 1, wx.ALL, 0)
        
        box.Add(box1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        okbut = wx.Button(self, wx.ID_OK, "Ok")
        okbut.SetDefault()
        oksizer.Add(okbut, 0, wx.RIGHT, 10)
        oksizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 0)
        box.Add(oksizer, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        box.Fit(self)
        box.SetSizeHints(self)
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        
        self.SetTime(_value)
        self.CentreOnParent(wx.BOTH)

    def SetTime(self, value=None):
        _value = datetime.datetime.now().time() if (value is None) else value
        self._h_ctrl.SetSelection(_value.hour)
        self._m_ctrl.SetSelection(_value.minute)
        if self.UseSecs:
            self._s_ctrl.SetSelection(_value.second)
    
    def GetTime(self):
        h = self._h_ctrl.GetSelection()
        m = self._m_ctrl.GetSelection()
        s = 0 if (not self.UseSecs) else self._s_ctrl.GetSelection()
        return datetime.time(h,m,s)
    
    def OnOk(self,event=None):
        _date = get_pydate(self.ctrl.GetValue())
        _time = self.GetTime()
        self.Value = datetime.datetime.combine(_date, _time)
        self.EndModal(wx.ID_OK)

    def OnCancel(self,event=None):
        self.EndModal(wx.ID_CANCEL)

#-----------------------------------------------------------------------------------------

class DateTimeGetter(object):
    """Callable: Presenta GetDateTimeDialog y retorna valor"""

    __slots__ = ('Title', 'Format', 'Vmin', 'Vmax', 'CtrlSize', 'CtrlStyle', 'UseSecs',
                 'Msg')
    
    def __init__(self, title="DateTime", format=None, vmin=None, vmax=None, ctrlSize=None,
                 ctrlStyle=None, useSecs=False, msg=None
                 ):
        """ 
        """
        self.Title = title
        self.Format = "%d/%m/%Y %H:%M" if format is None else format
        self.Vmin = vmin
        self.Vmax = vmax
        self.CtrlSize = ctrlSize
        self.CtrlStyle = ctrlStyle
        self.UseSecs = useSecs
        self.Msg = msg

    def GetText(self, value):
        if value is None:
            return ""
        return format_datetime(value, self.Format)
    
    def __call__(self, parent, value=None):
        dlg = GetDateTimeDialog(parent, self.Title, value, self.Vmin, self.Vmax,
                                self.CtrlSize, self.CtrlStyle, self.UseSecs, self.Msg)
        value = dlg.Value if dlg.ShowModal() == wx.ID_OK else None
        dlg.Destroy()
        return value

#-----------------------------------------------------------------------------------------

def get_datetime(parent, title="DateTime", value=None, vmin=None, vmax=None,
                 ctrlSize=None, ctrlStyle=None, useSecs=False, msg=None):
    """Presenta diálgo y retorna datetime.date seleccionado o None"""
    getter = DateTimeGetter(title, None, vmin, vmax, ctrlSize, ctrlStyle, useSecs, msg)
    return getter(parent, value)