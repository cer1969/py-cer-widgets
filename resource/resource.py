# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import wx, os, io

#-----------------------------------------------------------------------------------------

__all__ = ['get_font_data','get_file_data','get_image_data',
           'Resource','FontResource','ImageResource']

#-----------------------------------------------------------------------------------------
# Se requiere instancia de wx.App para poder usar las funciones

if not wx.GetApp():
    app = wx.App()

#-----------------------------------------------------------------------------------------
# Funciones para obtener data

def get_font_data(font):
    """Devulve data en formato compatible con FontResource
    font: Objeto wx.Font
    """
    pointSize = font.GetPointSize()
    family    = font.GetFamily()
    style     = font.GetStyle()
    weight    = font.GetWeight()
    underline = font.GetUnderlined()
    faceName  = font.GetFaceName()
    return (faceName, pointSize, weight, style, underline, family)


def get_file_data(filename, mode="r"):
    """Devuelve data de archivo.
    filename: Path del archivo
    mode: Modo de lectura. Puede ser r o rb.
    """
    f = open(filename,mode)
    data = f.read()
    f.close()
    return data

def get_image_data(filename, mask=None, type_=wx.BITMAP_TYPE_PNG, raw=False):
    """Devuelve data de imagen compatible con ImageResource
    filename: Path del archivo
    mask: Mask de transparencia para aplicar a bmp
    type_: Tipo de imagen para la data
    raw: Si es true se lee archivo en modo binario sin transformaciones
    """
    if raw:
        # Si es raw ignora mask e type_
        data = get_file_data(filename, "rb")
    else:
        # Lee el archivo de imagen
        img = wx.Bitmap(filename, wx.BITMAP_TYPE_ANY)
        
        # Aplica mask si corresponde
        if not(mask is None):
            om = img.GetMask()
            nMask = wx.Mask(img,mask)
            img.SetMask(nMask)
            if om is not None: 
                om.Destroy()
        
        # Graba archivo temporal con formato indicado
        tfname = "certempo_imagetemp.png"
        img.SaveFile(tfname, type_)
        
        # recupera data y elimina archivo temporal
        data = get_file_data(tfname, "rb")
        os.remove(tfname)
    return data

#-----------------------------------------------------------------------------------------

class Resource(object):
    """Clase base para Resources"""
    
    __slots__ = ('_dat',)
    
    def __init__(self, data):
        self._dat = data
    
    def _getData(self):
        return self._dat
    Data = property(_getData)

#-----------------------------------------------------------------------------------------

class FontResource(Resource):
    """Clase para menejo de Font Resources"""
    
    __slots__ = ('_font')
                    
    def __init__(self, faceName, 
                       pointSize,
                       weight    = wx.FONTWEIGHT_NORMAL,
                       style     = wx.FONTSTYLE_NORMAL,
                       underline = False,
                       family    = wx.FONTFAMILY_SWISS):
        data = (pointSize, family, style, weight, underline, faceName)
        Resource.__init__(self, data)
        self._font = None
        
    def _getFont(self):
        if self._font is None:
            self._font = wx.Font(*self.Data)
        return self._font
    Font = property(_getFont)

#-----------------------------------------------------------------------------------------

class ImageResource(Resource):
    """Clase para menejo de Font Resources"""
    
    __slots__ = ('_img', '_bmp', '_ico')
    
    def __init__(self, data):
        Resource.__init__(self,data)
        self._img = None
        self._bmp = None
        self._ico = None
    
    def _getImage(self):
        if self._img is None:
            stream = io.BytesIO(self.Data)
            self._img = wx.ImageFromStream(stream)
        return self._img
    Image = property(_getImage)

    def _getBitmap(self):
        if self._bmp is None:
            self._bmp = wx.BitmapFromImage(self.Image)
        return self._bmp
    Bitmap = property(_getBitmap)
    
    def _getIcon(self):
        if self._ico is None:
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(self.Bitmap)
            self._ico = icon
        return self._ico
    Icon = property(_getIcon)


#-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    data = get_image_data("Nuvola/cw_tb_tabla.bmp","#804000")

    imr = ImageResource(data)
    print (imr.Image)
    print (imr.Icon)
    
    fnr = FontResource("Tahoma",8,wx.BOLD)
    print (fnr.Font)