# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['ObjChoice']

#-----------------------------------------------------------------------------------------

class ObjChoice(wx.Choice):
    
    def __init__(self, parent, choices, attr, nosel=None, size=(-1,-1)):
        """
        choices : List with object to select.
        attr    : Objects Attribute to show
        nosel   : If None the selection is forced to one element of choices.
                  If diferent it must be a string to show as a first option 
        """
        wx.Choice.__init__(self, parent, size=size)
        self.attr = attr
        self.SetChoices(choices, nosel)
    
    def SetChoices(self, choices, nosel=None):
        self.Clear()
        
        if not(nosel is None):
            self.Append(nosel, None)
        
        for i in choices:
            name = getattr(i, self.attr)
            self.Append(name, i)
    
    def GetObjSelection(self):
        return self.GetClientData(self.GetSelection())