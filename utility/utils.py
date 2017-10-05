import re
import Queue
import logging
import threading
from django.conf import settings
from django.core.mail import send_mail


email_queue = Queue.Queue()
logger = logging.getLogger('email_logs')

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

def unslugify(string):
    names = string.split("-")
    return " ".join([x.title() for x in names])

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



class SendMail(object):
    def __init__(self):
        self.subject = ''
        self.text_content = ''
        self.html_content = ''
        self.from_mail = ''
        self.show_recipients = True
        self.bcc_address = []
        self.attachments = []
        self.recipient_list = []


    def set_params(self, **kwargs):
        self.subject = kwargs.get('subject','Test Mail')
        self.text_content = kwargs.get('text_content','')
        self.html_content = kwargs.get('html_content','')
        self.show_recipients = kwargs.get('show_recipients', True)
        self.from_mail = kwargs.get('from_mail',settings.DEFAULT_EMAIL_FROM)
        self.attachments = kwargs.get('attachments',[])
        self.bcc_address = kwargs.get('bcc_address',[])
        self.recipient_list = kwargs.get('recipient_list',[])
        self.set_daemon = kwargs.get('set_daemon',True)

        if type(self.attachments) in (str, unicode):
            self.attachments = [x.strip() for x in self.attachments.split(',') if x.strip()]
        else:
            self.attachments = list(self.attachments)

        if type(self.bcc_address) in (str, unicode):
            self.bcc_address = [x.strip() for x in self.bcc_address.split(',') if x.strip()]
        else:
            self.bcc_address = list(self.bcc_address)

        if type(self.recipient_list) in (str, unicode):
            self.recipient_list = [x.strip() for x in self.recipient_list.split(',') if x.strip()]
        else:
            self.recipient_list = list(self.recipient_list)


    def send_mail(self):
        try:
            send_mail(
                self.subject, 
                self.text_content,
                settings.EMAIL_HOST_USER, 
                self.recipient_list,
                fail_silently=False,
                html_message=self.html_content, 
            )
            success_message = "Mail sucessfully sent to recipients %s" % (', '.join(self.recipient_list))
            logger.info(success_message)
            
        except Exception as e:
            error_message = "Mail delivery failed for recipients %s, reason: " % (', '.join(self.recipient_list)) + str(e)
            logger.error(error_message)
