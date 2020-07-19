from functools import wraps
from uuid import uuid4
from xml.etree.ElementTree import tostring as ET_tostring

class letter_calc():
    _letter_dict1 = { chr(i):(i-ord('a')+1) for i in range(ord('a'),ord('z')+1)}
    _letter_dict2 = { (i-ord('a')+1):chr(i) for i in range(ord('a'),ord('z')+1)}

    def letter_next(self, letter):
        count = self._count(letter)
        print(count)
        i = count + 1
        s = ''
        while i != 0:
            s = self._letter_dict2[i%26] + s
            i = i // 26
        return s

    def _count(self, s):
        p = len(s) - 1
        count = 0
        for x in range(len(s)):
            count += (26**x)*self._letter_dict1[s[p-x]]
        return count

def addDoc(doctext):
    def handle_func(func):
        @wraps(func)
        def handle_args(*args, **kwargs):
            return func(*args, **kwargs)
        handle_args.__doc__ = doctext
        return handle_args
    return handle_func

def uuidgen(): return str(uuid4())

def map_tuple_or_str(k):
    if type(k) == tuple:
        return k[0]
    else:
        return k

def getClassName(obj): return type(obj).__name__

def prettyXML(obj, level = 1):
    i = len(obj)
    if i > 0:
        for n in obj:
            prettyXML(n,level+1)
        obj.text = '\n' + ' '*level*2
        obj.tail = '\n' + ' '*(level-1)*2
        obj[-1].tail = '\n' + ' '*(level-1)*2
    else:
        obj.tail = '\n' + ' '*(level-1)*2
    return ET_tostring(obj,encoding='UTF-8').decode('UTF-8')[:-1]

MEMORY_UNITS=['B', 'K', 'M', 'G', 'T', 'P']
def formatHumanReadMemory(hr, aimunit):
    value = hr[:-1]
    unit = hr[-1].upper()
    if not value.isnumeric():
        raise ValueError('Wrong format! "%s" don\'t match "\d+\w".' % hr)
    value = int(value)
    if unit not in MEMORY_UNITS:
        raise ValueError('UnSupport unit! Unit only support [B,K,M,G,T,P] but not "%s"' % unit)
    aimi = MEMORY_UNITS.index(aimunit.upper())
    ui = MEMORY_UNITS.index(unit)
    rsp = value * 1024 ** (ui-aimi)
    return int(rsp) if rsp % 1 == 0 else rsp
