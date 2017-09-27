import re

class Mask(object):
    """
    This class accepts 2 params:
        name -> the name to be masked
        mask_flag -> boolean (decides whether name should be masked or not)
    """
    def __init__(self, name, mask_flag = True, maskcharacter = '*'):
        self.name = name
        self.mask_flag = mask_flag
        self.maskcharacter = maskcharacter

    def partial_masking(self):
        """
        displays the first 2 and last 2 letters and masks the remaining letters in between

        """
        if self.mask_flag:
            return "%s%s%s" % (self.name[:2], self.maskcharacter * len(self.name[2:-2]), self.name[-2:])
        return self.name


    def complete_masking(self):
        """
        masks all the letters in name

        """
        if self.mask_flag:
            return "%s" % (self.maskcharacter * len(self.name),)
        return self.name



class ComputeCompletion(object):
    """
    accept a model obj, and compute the percentage of columns containing data by iterating through it

    """
    def __init__(self, data):
        if data:
            self.data = data[0]
            self.data_length = len(self.data)
        else:
            self.data_length = 0

    def compute_percent(self):
        denominator = self.data_length
        numerator = sum([ 1 for k,v in self.data.items() if v not in (None, '', 0) ])
        percent = "%d" % ((numerator * 100 / denominator), )
        if percent < 20:
            percent = 20
        
        percent = "%s%s" %(percent, "%")
        return percent

from urllib import urlencode
def get_prefix(name=None):
    """
    if sort=data, then return None
    elif sort=-data, then return '-'

    """
    try:
        return '-' if name[0] != '-' else ''
    except:
        return ''


def form_url(url, getparams, key, val):
    surl = url.split("?")
    if len(surl) > 1:
        for qp in surl[1].split("&"):
            if qp:
                x = qp.split("=")
                getparams.update({
                    x[0]:x[1]
                })
    getparams.update({
        key:val
    })

    return "%s?%s" % (surl[0], urlencode(getparams))


class NoDefaultProvided(object):
    pass

def getattrd(obj, name, default=NoDefaultProvided):
    """
    Same as getattr(), but allows dot notation lookup
    Discussed in:
    http://stackoverflow.com/questions/11975781
    """

    try:
        return reduce(getattr, name.split("."), obj)
    except AttributeError, e:
        if default != NoDefaultProvided:
            return default
    except Exception:
        return None


def getobj(model, value):
    x = model.objects.filter(slug=value)
    if not x:
        return model.objects.filter(id=99999)
    return x[0]

def slugify(string):
    newstr = string.lower().replace(" ","-")
    return re.sub('[^a-zA-Z0-9-]', '', newstr)


def null_to_empty(func):
    def inner(*args, **kwargs):
        value = func(*args, **kwargs)
        if value and value not in ("null",):
            return value
        else:
            return ""

    return inner


def substring(string, start):
    i = string.index(start)
    return string[i:]
