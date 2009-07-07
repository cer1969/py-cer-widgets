# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import wx

#-----------------------------------------------------------------------------------------

__all__ = ['Clipboard']
        
#-----------------------------------------------------------------------------------------

class Clipboard(object):

    @staticmethod
    def GetText():
        wx.TheClipboard.Open()
        clipdata = wx.TextDataObject()
        wx.TheClipboard.GetData(clipdata)
        wx.TheClipboard.Close()
        return clipdata.GetText()

    @staticmethod
    def SetText(text):
        wx.TheClipboard.Open()
        clipdata = wx.TextDataObject(text)
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()

    @staticmethod
    def GetTextTable(dataSep="\t",lineSep="\n",repList=[]):
        text = Clipboard.GetText()
        text = text.replace("\r","")
        if repList:
            for oldText,newText in repList:
                text = text.replace(oldText,newText)

        filas = text.split(lineSep)
        sal = []
        for i in filas:
            if i: sal.append(i.split(dataSep))
        return sal

    @staticmethod
    def GetFloatTable(dataSep="\t",lineSep="\n",repList=[]):
        data = Clipboard.GetTextTable(dataSep,lineSep,repList)
        sal = []
        for i in data:
            fila = []
            for j in i:
                try: val = float(j)
                except ValueError: val=j
                fila.append(val)
            sal.append(fila)
        return sal