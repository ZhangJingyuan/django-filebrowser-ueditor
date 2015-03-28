# coding: utf-8

# PYTHON IMPORTS
import re
import os
import unicodedata

# DJANGO IMPORTS
from django.utils import six

# FILEBROWSER IMPORTS
from filebrowser_ueditor.settings import STRICT_PIL, NORMALIZE_FILENAME, CONVERT_FILENAME

# PIL import
if STRICT_PIL:
    from PIL import Image
else:
    try:
        from PIL import Image
    except ImportError:
        import Image


def convert_filename(value):
    """
    Convert Filename.
    """

    if NORMALIZE_FILENAME:
        chunks = value.split(os.extsep)
        normalized = []
        for v in chunks:
            v = unicodedata.normalize('NFKD', six.text_type(v)).encode('ascii', 'ignore').decode('ascii')
            v = re.sub(r'[^\w\s-]', '', v).strip()
            normalized.append(v)

        if len(normalized) > 1:
            value = '.'.join(normalized)
        else:
            value = normalized[0]

    if CONVERT_FILENAME:
        value = value.replace(" ", "_").lower()

    return value


def path_strip(path, root):
    if not path or not root:
        return path
    path = os.path.normcase(path)
    root = os.path.normcase(root)
    if path.startswith(root):
        return path[len(root):]
    return path


def scale_and_crop(im, width, height, opts):
    """
    Scale and Crop.
    """

    x, y = [float(v) for v in im.size]

    if 'upscale' not in opts and x < width:
        # version would be bigger than original
        # no need to create this version, because "upscale" isn't defined.
        return False

    if width:
        xr = float(width)
    else:
        xr = float(x*height/y)
    if height:
        yr = float(height)
    else:
        yr = float(y*width/x)

    if 'crop' in opts:
        r = max(xr/x, yr/y)
    else:
        r = min(xr/x, yr/y)

    if r < 1.0 or (r > 1.0 and 'upscale' in opts):
        im = im.resize((int(x*r), int(y*r)), resample=Image.ANTIALIAS)

    if 'crop' in opts:
        x, y = [float(v) for v in im.size]
        ex, ey = (x-min(x, xr))/2, (y-min(y, yr))/2
        if ex or ey:
            im = im.crop((int(ex), int(ey), int(x-ex), int(y-ey)))
    return im

scale_and_crop.valid_options = ('crop', 'upscale')

#ueditor function
#文件大小类
class FileSize():
    SIZE_UNIT={"Byte":1,"KB":1024,"MB":1048576,"GB":1073741824,"TB":1099511627776L}
    def __init__(self,size):
        self.size=long(FileSize.Format(size))

    @staticmethod
    def Format(size):
        import re
        if isinstance(size,int) or isinstance(size,long):
            return size
        else:
            if not isinstance(size,str):
                return 0
            else:
                oSize=size.lstrip().upper().replace(" ","")
                pattern=re.compile(r"(\d*\.?(?=\d)\d*)(byte|kb|mb|gb|tb)",re.I)
                match=pattern.match(oSize)
                if match:
                    m_size, m_unit=match.groups()
                    if m_size.find(".")==-1:
                        m_size=long(m_size)
                    else:
                        m_size=float(m_size)
                    if m_unit!="BYTE":
                        return m_size*FileSize.SIZE_UNIT[m_unit]
                    else:
                        return m_size
                else:
                    return 0

    #返回字节为单位的值
    @property
    def size(self):
        return self.size
    @size.setter
    def size(self,newsize):
        try:
            self.size=long(newsize)
        except:
            self.size=0

    #返回带单位的自动值
    @property
    def FriendValue(self):
        if self.size<FileSize.SIZE_UNIT["KB"]:
            unit="Byte"
        elif self.size<FileSize.SIZE_UNIT["MB"]:
            unit="KB"
        elif self.size<FileSize.SIZE_UNIT["GB"]:
            unit="MB"
        elif self.size<FileSize.SIZE_UNIT["TB"]:
            unit="GB"
        else:
            unit="TB"

        if (self.size % FileSize.SIZE_UNIT[unit])==0:
            return "%s%s" % ((self.size / FileSize.SIZE_UNIT[unit]),unit)
        else:
            return "%0.2f%s" % (round(float(self.size) /float(FileSize.SIZE_UNIT[unit]) ,2),unit)

    def __str__(self):
        return self.FriendValue

    #相加
    def __add__(self, other):
        if isinstance(other,FileSize):
            return FileSize(other.size+self.size)
        else:
            return FileSize(FileSize(other).size+self.size)
    def __sub__(self, other):
        if isinstance(other,FileSize):
            return FileSize(self.size-other.size)
        else:
            return FileSize(self.size-FileSize(other).size)
    def __gt__(self, other):
        if isinstance(other,FileSize):
            if self.size>other.size:
                return True
            else:
                return False
        else:
            if self.size>FileSize(other).size:
                return True
            else:
                return False
    def __lt__(self, other):
        if isinstance(other,FileSize):
            if other.size>self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size > self.size:
                return True
            else:
                return False
    def __ge__(self, other):
        if isinstance(other,FileSize):
            if self.size>=other.size:
                return True
            else:
                return False
        else:
            if self.size>=FileSize(other).size:
                return True
            else:
                return False
    def __le__(self, other):
        if isinstance(other,FileSize):
            if other.size>=self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size >= self.size:
                return True
            else:
                return False

