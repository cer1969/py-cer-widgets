# CRISTIAN ECHEVERRÍA RABÍ

import wx
import datetime

#-----------------------------------------------------------------------------------------

__all__ = ['format_time','GetTimeDialog', 'TimeGetter', 'get_time']

#-----------------------------------------------------------------------------------------

def format_time(myTime, format="%H:%M"):
    """Formatea datetime.time
    myTime: datetime.time object.
    format: string de formato para strftime.
    """
    return myTime.strftime(format)

_K_RANGE24 = ["%02d" % x for x in range(24)]
_K_RANGE60 = ["%02d" % x for x in range(60)]

#-----------------------------------------------------------------------------------------

class GetTimeDialog(wx.Dialog):
    """Cuadro de diálogo para ingreso de tiempo"""
    
    def __init__(self, parent, title="Date", value=None, vmin=None, vmax=None, 
                 useSecs=False, msg=None
                 ):
        """
        """
        wx.Dialog.__init__(self, parent, -1, title)
        
        self.Value = None
        self.Vmin = datetime.time.min if vmin is None else vmin
        self.Vmax = datetime.time.max if vmax is None else vmax
        self.UseSecs = useSecs
        _msg = title if msg is None else msg
        self._errmsg = "Time requiered\nRange\t: [%s, %s]" % (self.Vmin, self.Vmax)
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        st = wx.StaticText(self, -1, _msg)
        box.Add(st, 0, wx.EXPAND|wx.ALL, 10)
        
        self._h_ctrl = wx.Choice(self, choices=_K_RANGE24)
        self._m_ctrl = wx.Choice(self, choices=_K_RANGE60)
        
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self._h_ctrl, 0, wx.ALL, 0)
        box1.Add(wx.StaticText(self,-1,":"), 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        box1.Add(self._m_ctrl, 0, wx.ALL,0)
        
        if useSecs:
            self._s_ctrl = wx.Choice(self, choices=_K_RANGE60)
            box1.Add(wx.StaticText(self,-1,":"), 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,2)
            box1.Add(self._s_ctrl, 0, wx.ALL, 0)
        
        box.Add(box1, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 10)
        
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        okbut = wx.Button(self, wx.ID_OK, "Ok")
        okbut.SetDefault()
        oksizer.Add(okbut, 0, wx.RIGHT, 10)
        oksizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 0)
        box.Add(oksizer,0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        box.Fit(self)
        box.SetSizeHints(self)
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        
        self.SetTime(value)
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
        t = self.GetTime()
        
        errFlag = False
        if not(self.Vmin is None) and t < self.Vmin:
            errFlag = True
        if not(self.Vmax is None) and t > self.Vmax:
            errFlag = True
        
        if errFlag:
            wx.MessageBox(self._errmsg, "Error", wx.ICON_ERROR|wx.OK, parent=self)
            return
        
        self.Value = t
        self.EndModal(wx.ID_OK)

    def OnCancel(self,event=None):
        self.EndModal(wx.ID_CANCEL)

#-----------------------------------------------------------------------------------------
                 
class TimeGetter(object):
    """Callable: Presenta GetTimeDialog y retorna valor"""
    
    __slots__ = ('Title', 'Format', 'Vmin', 'Vmax', 'UseSecs', 'Msg')
    
    def __init__(self, title="Time", format=None, vmin=None, vmax=None, useSecs=False,
                 msg=None
                 ):
        """ 
        """
        self.Title = title
        self.Format = "%H:%M" if format is None else format
        self.Vmin = vmin
        self.Vmax = vmax
        self.UseSecs = useSecs
        self.Msg = msg

    def GetText(self,value):
        if value is None:
            return ""
        return format_time(value, self.Format)
    
    def __call__(self, parent, value=None):
        dlg = GetTimeDialog(parent, self.Title, value, self.Vmin, self.Vmax, self.UseSecs, self.Msg)
        value = dlg.Value if dlg.ShowModal() == wx.ID_OK else None
        dlg.Destroy()
        return value

#-----------------------------------------------------------------------------------------

def get_time(parent, title="Time", value=None, vmin=None, vmax=None, useSecs=False, 
             msg=None):
    """Presenta diálgo y retorna datetime.time seleccionado o None"""
    getter = TimeGetter(title, None, vmin, vmax, useSecs, msg)
    return getter(parent, value)
