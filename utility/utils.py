import re
import Queue
import logging
import threading
from django.core import mail
from django.conf import settings
from compiler.ast import flatten
from smtplib import SMTPException
#from leadinfo.models import LeadDetail, CallHistory
from django.core.mail import EmailMultiAlternatives


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
        self.from_mail = kwargs.get('from_mail',settings.DEFAULT_FROM_EMAIL)
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
            email_data = self.__dict__
            email_queue.put(email_data)
            email_thread = threading.Thread(target=send_queued_mails,)
            if self.set_daemon:
                email_thread.setDaemon(True)
            email_thread.start()
        except Exception, e:
            error_message = "Mail delivery failed for recipients %s, reason: %s" % (', '.join(self.recipient_list), str(e))
            logger.debug(error_message)
            #print error_message


def send_queued_mails():
    data = email_queue.get()
    try:
        if data['show_recipients']:
            msg = create_email(data)
        else:
            connection = mail.get_connection()
            connection.open()
            messages = list()
            for recipient in data['recipient_list']:
                msg = create_email(data,recipient)
                if msg:
                    messages.append(msg)

        if data['show_recipients']:
            response = msg.send(fail_silently=False)
        else:
            response = connection.send_messages(messages)
            connection.close()
        success_message = "Mail sucessfully sent to recipients %s" % (', '.join(list(flatten(data['recipient_list']))))
        #print response, success_message
        logger.info(response)
        logger.info(success_message)

    except SMTPException as e:
        error_message = "Mail delivery failed for recipients %s, reason: " % (', '.join(list(flatten(data['recipient_list'])))) + str(e)
        logger.error(error_message)

    except Exception as e:
        error_message = "Mail delivery failed for recipients %s, reason: %s" % (', '.join(list(flatten(data['recipient_list']))), str(e))
        logger.error(error_message)



def create_email(data,recipient=''):
    if recipient:
        receiver_mail = recipient[0] if recipient.__class__.__name__ == 'tuple' else recipient
        # Code for sending personalized messages to each user and Code for sending same message to each user
        msg_body = data['text_content'] % (recipient[1:]) if recipient.__class__.__name__ == 'tuple' else data['text_content']
        msg = EmailMultiAlternatives(data['subject'], msg_body, data['from_mail'], [receiver_mail], bcc=data['bcc_address'])
    else:
        msg = EmailMultiAlternatives(data['subject'], data['text_content'], data['from_mail'], data['recipient_list'], bcc=data['bcc_address'])
    if data['html_content']:
        msg.attach_alternative(data['html_content'], "text/html")

    try:
        if len(data['attachments']) > 0:
            for file_name in data['attachments']:
                attachment = os.path.join(settings.ATTACHMENT_PATH, '%s' % file_name).replace('\\', '/')
                msg.attach_file(attachment)
    except Exception as e:
        if recipient:
            error_message = "Mail creation failed for recipient %s, reason: %s" % (recipient, str(e))
        else:
            error_message = "Mail creation failed for recipients %s, reason: %s" % (', '.join(list(flatten(data['recipient_list']))), str(e))
        logger.error(error_message)

    else:
        return msg
    return None
