# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import glob, os, py_compile
import wx
from .resource import get_font_data, get_file_data, get_image_data

#-----------------------------------------------------------------------------------------

__all__ = ['ResourceMaker','PNG','JPG','RESJAVA','RESWX','RESNUVOLA']

#-----------------------------------------------------------------------------------------

PNG = wx.BITMAP_TYPE_PNG
JPG = wx.BITMAP_TYPE_JPEG

#-----------------------------------------------------------------------------------------

class ResourceMaker(object):
    """Crea archivos ResourceManager"""

    __slots__ = ('_imgData','_imgListData','_strData','_fontData')
    
    def __init__(self):
        self._imgData = {}
        self._imgListData = {}
        self._strData = {}
        self._fontData = {}

    #-------------------------------------------------------------------------------------
    # Métodos relacionados con recursos de imagen

    def AddStdImageDir(self, dir, ext, mask=None, type_=PNG, raw=False):
        """Agrega imágenes de directorio standard"""
        modpath = os.path.abspath(__file__)
        moddir, _modfile = os.path.split(modpath)
        imgdir = os.path.join(moddir, dir)
        self.AddImageDir(imgdir, ext, mask, type_, raw)
        
    def AddImageDir(self, dir, ext, mask=None, type_=PNG, raw=False):
        """Agrega directorio de imagenes personal"""
        lista = glob.glob(os.path.join(dir, ext))
        for i in lista:
            self.AddImageFile(i, mask, type_, raw)
        
    def AddImageFile(self, filename, mask=None, type_=PNG, raw=False):
        """Agrega imagen individual"""
        name, _ext = os.path.splitext(os.path.basename(filename))
        self._imgData[name] = (filename, mask, type_, raw)

    #-------------------------------------------------------------------------------------
    # Métodos relacionados con ImageList
    # TODO: Reemplazar width, height por tuple
    
    def AddImageList(self, name, width, height, imgnames):
        """Datos para creación de wx.ImageList"""
        self._imgListData[name] = (width, height, imgnames)
        
    #-------------------------------------------------------------------------------------
    # Métodos relacionados con recursos de string

    def AddString(self, name, text):
        self._strData[name] = text

    def AddStringPyFile(self, filename):
        """Agrega o reemplaza strings de archivo con sintaxis de Python"""
        mydict = {}
        execfile(filename, {}, mydict)
        self._strData.update(mydict)

    def AddStringDir(self, strdir, fullName=True):
        lista = glob.glob(os.path.join(strdir, "*.*"))
        for i in lista:
            self.AddStringFile(i, fullName)

    def AddStringFile(self, filename, fullName=True):
        # TODO: Modificar considerando un encoding como parámetro
        """Agrega contenido completo de un archivo como un solo string
           Si fullName es True, la key será el nombre del archivo con extensión
        """
        name = os.path.basename(filename)
        if not fullName:
            name, _ext = os.path.splitext(name)
        data = get_file_data(filename, "r")
        self._strData[name] = data

    #-------------------------------------------------------------------------------------
    # Métodos relacionados con recursos de Fuentes

    def AddFont(self, name, font):
        data = get_font_data(font)
        self._fontData[name] = data

    def AddFontData(self, name, faceName, 
                                pointSize,
                                weight    = wx.FONTWEIGHT_NORMAL,
                                style     = wx.FONTSTYLE_NORMAL,
                                underline = False,
                                family    = wx.FONTFAMILY_SWISS):
        self._fontData[name] = (faceName, pointSize, weight, style, underline, family)
    
    def AddStdFonts(self):
        self.AddFontData("std08", "Tahoma", 8)
        self.AddFontData("std08b", "Tahoma", 8, wx.FONTWEIGHT_BOLD)
        self.AddFontData("std10", "Tahoma", 10)
        self.AddFontData("std10b", "Tahoma", 10, wx.FONTWEIGHT_BOLD)
        self.AddFontData("std12", "Tahoma", 12)
        self.AddFontData("std12b", "Tahoma", 12, wx.FONTWEIGHT_BOLD)
        
    #-------------------------------------------------------------------------------------
    # Métodos Generales

    def UpdateImages(self, resMaker, imgNames=[]):
        """Agrega o reemplaza nombres usando otro CerResourceMaker"""
        if imgNames:
            for i in imgNames:  self._imgData[i]  = resMaker._imgData[i]
        else:
            self._imgData.update(resMaker._imgData)

    def UpdateStrings(self, resMaker, strNames=[]):
        """Agrega o reemplaza nombres usando otro CerResourceMaker"""
        if strNames:
            for i in strNames:  self._strData[i]  = resMaker._strData[i]
        else:
            self._strData.update(resMaker._strData)

    def UpdateFonts(self, resMaker, fontNames=[]):
        """Agrega o reemplaza nombres usando otro CerResourceMaker"""
        if fontNames:
            for i in fontNames: self._fontData[i] = resMaker._fontData[i]
        else:
            self._fontData.update(resMaker._fontData)

    def UpdateAll(self, resMaker):
        """Agrega o reemplaza nombres usando otro CerResourceMaker"""
        self._imgData.update(resMaker._imgData)
        self._strData.update(resMaker._strData)
        self._fontData.update(resMaker._fontData)

    #-------------------------------------------------------------------------------------
    
    def Make(self, filename):
        """Crea el archivo de recursos con el nombre filename
        """
        # datos de imágenes
        txtImg = "imgData = {}\n"
        for name, args in self._imgData.items():
            data = get_image_data(*args)
            txt = "imgData['%s'] = %s\n" % (name, repr(data))
            txtImg = txtImg + txt

        # datos de ImageList
        txtImgList = "imgListData = {}\n"
        for name, data in self._imgListData.items():
            txt = "imgListData['%s'] = %s\n" % (name, data)
            txtImgList = txtImgList + txt

        # datos de Strings
        txtStr = "strData = {}\n"
        for name, texto in self._strData.items():
            txt = "strData['%s'] = %s\n" % (name, repr(texto))
            txtStr = txtStr + txt

        # datos de Fuentes
        txtFont = "fontData = {}\n"
        for name, font in self._fontData.items():
            txt = "fontData['%s'] = %s\n" % (name, font)
            txtFont = txtFont + txt

        sal = RES_TEMPLATE % (txtImg, txtImgList, txtStr, txtFont)

        f = open(filename, "w")
        f.write(sal)
        f.close()

        py_compile.compile(filename)
        print ("Terminado")

#-----------------------------------------------------------------------------------------
# Plantilla de archivo de recursos

RES_TEMPLATE = """# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ
# Archivo de recursos creado usando cg.ResourceMaker
from cer.widgets.resource import ResourceManager

#-----------------------------------------------------------------------------------------

%s
%s
%s
%s
#-----------------------------------------------------------------------------------------

resman = ResourceManager(imgData, imgListData, strData, fontData)
"""

#-----------------------------------------------------------------------------------------
# Objetos para crear algunos recursos standard

RESJAVA = ResourceMaker()
RESJAVA.AddStdImageDir("java", "*.png", raw=True)
RESJAVA.AddStdFonts()

RESWX = ResourceMaker()
RESWX.AddStdImageDir("wx", "*.bmp", "#804000")
RESWX.AddStdFonts()

RESNUVOLA = ResourceMaker()
RESNUVOLA.AddStdImageDir("nuvola", "*.bmp", "#804000")
RESNUVOLA.AddStdImageDir("nuvola", "*.png", raw=True)
RESNUVOLA.AddStdFonts()

#-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    RESJAVA.Make("rxjava.py")
    RESWX.Make("rxwx.py")
    RESNUVOLA.Make("rxnuvola.py")