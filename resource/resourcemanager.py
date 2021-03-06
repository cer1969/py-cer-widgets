# CRISTIAN ECHEVERRÍA RABÍ

import wx
from .resource import Resource, FontResource, ImageResource

#-----------------------------------------------------------------------------------------

__all__ = ['ResourceManager']

#-----------------------------------------------------------------------------------------

class ResourceManager(object):
    
    __slots__ = ('_imgs','_imgListData','_imgLists','_strs','_fonts')

    def __init__(self, imgData={}, imgListData={}, strData={}, fontData={}):
        
        imgs = {}
        for name, data in list(imgData.items()):
            imgs[name] = ImageResource(data)
        self._imgs = imgs
        
        self._imgListData = imgListData
        self._imgLists = {}
        
        strs = {}
        for name, data in list(strData.items()):
            strs[name] = Resource(data)
        self._strs = strs
        
        fonts = {}
        for name, data in list(fontData.items()):
            fonts[name] = FontResource(*data)
        self._fonts = fonts
    
    #-------------------------------------------------------------------------------------

    def Image(self, name):
        return self._imgs[name].Image

    def ImageList(self, name):
        if name not in self._imgLists:
            w, h, imn = self._imgListData[name]
            il = wx.ImageList(w, h, True)
            for i in imn:
                bmp = self.Bitmap(i, (w, h))
                il.Add(bmp)
            self._imgLists[name] = il
        return self._imgLists[name]
    
    def Bitmap(self, name, size=(16, 16)):
        if name in self._imgs:
            return self._imgs[name].Bitmap
        else:
            # Busquemos en el wxArtProvider
            # Si no se encuentra en wxArtProvider se obtiene Bitmap nulo
            artName = "wxART_%s" % name[3:].upper()
            bmp = wx.ArtProvider.GetBitmap(artName, size=size)
            return bmp
    
    def Icon(self, name, size=(16, 16)):
        if name in self._imgs:
            return self._imgs[name].Icon
        else:
            bmp = self.Bitmap(name, size)
            icon = wx.Icon()
            icon.CopyFromBitmap(bmp)
            return icon
    
    def String(self,nombre):
        return self._strs[nombre].Data

    def Font(self,nombre):
        return self._fonts[nombre].Font