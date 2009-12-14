# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['DataCtrl']

#-----------------------------------------------------------------------------------------

class _ThisValidator(wx.PyValidator):
    # Validator para DataCtrl: Delega todo en el DataCtrl"""
    
    def Validate(self, win):
        return self.GetWindow().TestWindow()

    def TransferToWindow(self):
        return self.GetWindow().ToWindow() 
    
    def TransferFromWindow(self):
        return self.GetWindow().FromWindow()
    
    def Clone(self):
        return _ThisValidator()

#-----------------------------------------------------------------------------------------

class DataCtrl(wx.TextCtrl):
    
    def __init__(self, parent, cerValidator, data=None, size=(150,-1), style=0):
        """
        cerValidator : CerValidator object
        data         : Data value
        size         : Control size. Default (150, -1)
        style        : Control style. Default 0
        """
        
        self.CerValidator = cerValidator
        
        wx.TextCtrl.__init__(self, parent, -1, size=size, style=style, 
                             validator=_ThisValidator())
        
        if cerValidator.chars != "":
            self.Bind(wx.EVT_CHAR, self._onChar)
        
        # se debe llamar ToWindow() para actualizar
        # esto normalmente lo hace el validator
        self._data = data

    def _onChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in self.CerValidator.chars:
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        return
    
    def TestWindow(self):
        text = self.GetValue()
        try:
            _value = self.CerValidator.getData(text)
        except ValueError, e:
            wx.MessageBox(e[0],"Error",wx.ICON_ERROR|wx.OK,parent=self)
            self.SetBackgroundColour("Yellow")
            self.FocusControl()
            return False
        return True

    def ToWindow(self): 
        text = self.CerValidator.getText(self._data)
        self.SetValue(text)
        self.FocusControl()
        return True

    def FromWindow(self):
        try:
            text = self.GetValue()
            self._data = self.CerValidator.getData(text)
            return True
        except ValueError:
            self._data = None
            return False
    
    def FocusControl(self):
        """Set focus on inserted text"""
        self.SetFocus()
        val = self.GetValue()
        nch = len(val) + len(val.split("\n")) - 1
        self.SetSelection(0,nch)
        #self.Refresh()

    def _setData(self, data):
        self._data = data
        self.ToWindow()
    
    def _getData(self):
        self.FromWindow()
        return self._data
    
    Data = property(_getData, _setData)