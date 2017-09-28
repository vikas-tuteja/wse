# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django_redis import get_redis_connection
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse

from models import UserDetail, UserRole, CandidateAttribute
from utility.utils import ComputeCompletion, form_url, getobj, SendMail
from serializers import UserSerializer, AuthUserSerializer, UserMeterSerializer
from events.views import EventListing
from events.models import AllocationStatus
from events.serializers import ProfileEventSerializer
from utility import mygenerics
from utility.fields import AuthUserFields, UserDetailFields, CandidateAttributeFields, ClientAttributeFields
from utility.email_config import email_data as econf
from master.views import AreaList, CityList, StateList
from master.models import HighestQualification, Area, City
from users.choices import LOOKS, LANGUAGE_PROFICIENCY

from filters import UserFilters
from django.conf import settings

# Create your views here.

class CreateUser( generics.CreateAPIView ):
    """
    To create a new user, we require only 3 mandatory fields
    user name which will be the same as email
    password and 10 digit mobile 
    METHOD : POST
    POST PARAMS: email
               : password
               : user_role
               : mobile
               : type
    
    PS: if not password, then mobile = password
    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def post(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.POST.dict())
        
        # check if user already exists
        email = kwargs.get('username', kwargs.get('email'))
        mobile = kwargs.get('mobile')[-10:]
        exists = UserDetail.objects.filter(
            Q(auth_user__username=email) | Q(auth_user__email=email) | Q(mobile=mobile) 
        )

        if not exists:
            try:
                # create auth user first
                auth_user = User.objects.create(
                    username = email,
                    email = email,
                )
                auth_user.set_password(kwargs.get('password', kwargs.get('mobile')))
                auth_user.save()
                
                # then create userdetails
                user_role = kwargs.get('user_role', 'candidate')
                user_detail = UserDetail.objects.create(
                    auth_user = auth_user,
                    type = UserRole.objects.get(slug=user_role),
                    mobile = mobile,
                )
                user_detail.save()
            
                # automatic login after registration
                username = kwargs.get('username', kwargs.get('email'))
                password = kwargs.get('password', kwargs.get('mobile'))
                user = authenticate(
                    username = username,
                    password = password
                )
                auth_login(request, user)

                status = True
                message = 'User created successfully.'
                if not kwargs.get('password'):
                    message = 'User created successfully. <br>Login id is your email and mobile number is your password.'

                # welcome email
                email_data = econf.get(user_role)['welcome']
                html_content = email_data['html'] % {'username': username, 'password': password}

                emailobj = SendMail()
                emailobj.set_params(
                        recipient_list=username, 
                        subject=email_data['subject'],
                        text_content=email_data['plain_text'],
                        html_content=html_content,
                        attachments=[],
                        bcc_address=email_data['bcc_address'],
                        show_recipients=False,
                        set_daemon=False,
                )
                emailobj.send_mail()

            except IntegrityError:
                message = 'User with this email or mobile already exists '
        else:
            message = 'User with this email or mobile already exists '

        return JsonResponse(data={
            'status':status,
            'message':message
        })
        
class Logout( generics.ListAPIView ):
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        prev = request.META.get('HTTP_REFERER')
        if not prev or '/my-profile/' in prev:
            prev = reverse('home')
        prev = form_url(prev, request.GET.dict(), 'alert_message', 'Logged out successfully.')
        return HttpResponseRedirect(prev)

class LoginUser( generics.ListAPIView ):
    """
    METHOD : POST
    POST PARAMS: email
               : password
    """
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()
    
    def post(self, request, *args, **kwargs):
        kwargs.update(request.POST.dict())
        status = False
        user = authenticate( username = kwargs.get('username', kwargs.get('email')), password = kwargs.get('password') )

        if not user:
            message = 'Error: Invalid credentials'
        else:
            auth_login(request, user)
            status = True
            message = 'Successfully logged in'

        return JsonResponse( data={
            'status':status,
            'message':message,
        })


class ForgotPassword( generics.UpdateAPIView ):
    """
    this will change the password of the user to 
    his/her 10 digit mobile number
    METHOD : PUT
    POST PARAMS: email

    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def put(self, request, *args, **kwargs):
        status = False
        email = request.POST.get('username')
        if not email:
            message = 'Error: Please enter username.'

        else:
            try:
                userObj = UserDetail.objects.get(auth_user__email=email)
                if not userObj:
                    message = 'Error: %s user not found.' % email
                else:
                    userObj.auth_user.set_password( str(userObj.mobile)[-10:] )
                    userObj.auth_user.save()
                    status = True
                    message = 'Your new password is reset to your 10 digit mobile number.'
            except UserDetail.DoesNotExist:
                    message = 'User with this email does not exists. Please register first.'

        return JsonResponse(data={
            'status':status,
            'message':message
        })



class ChangePassword( generics.UpdateAPIView ):
    """
    changing the password to a new password
    METHOD : PUT
    POST PARAMS: email
               : password
               : new password
    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.none()
    lookup_field = "auth_user__email"
    lookup_url_kwarg = "user_email"

    def put(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.POST.dict())
        auth_user = authenticate( 
            username = kwargs.get('username'),
            password = kwargs.get('password')
        )
        #auth_login(request, auth_user)

        if not getattr(auth_user, 'email', None):
            message = 'Error: Old Password is incorrect'

        else:
            auth_user.set_password(kwargs.get('new_password'))
            auth_user.save()
            status, message = True, 'Password changed Successfully'

            # make user login again with new credentials
            auth_user = authenticate( 
                username = kwargs.get('username'),
                password = kwargs.get('new_password')
            )
            auth_login(request, auth_user)

        return JsonResponse(data={
            'status':status,
            'message':message
        })


class CheckUsernameExists( generics.ListAPIView ):
    """
    check in redis "key : usernames" if the user already exists with us
    return True if the username already exists, else False
    GET params : username
    
    """
    serializer_class = AuthUserSerializer
    queryset = UserDetail.objects.none()

    def get(self, request, *args, **kwargs ):

        status, message = False, str()
        username = request.GET.get('username')
        if not username:
            message = 'Invalid params: Please enter username'
        else:
            con = get_redis_connection('default')
            status = con.sismember("usernames", username)
            if status:
                message = "Error: Username already exists."

        return JsonResponse(data={
            'status':status,
            'message':message
        })


class UserProfileCompletionMeter( generics.ListAPIView ):
    """
    calculates the percentage of user profile completion
    input params: username
    output: a number that indicates the percentage of user profile competed
    logic : (no of column filled / total no of column ) * 100

    """
    serializer_class = UserMeterSerializer
    queryset = UserDetail.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilters

    def get(self, *args, **kwargs):
        response = super(UserProfileCompletionMeter, self).get(*args, **kwargs)
        try:
            candidate_info = response.data['results'][0]['candidate']
            del response.data['results'][0]['candidate']
            response.data['results'][0].update(candidate_info)
        except:
            pass

        # TODO get CANDIDATEATTRIBUTE all fileds + USERDETAIL ALL FIELDS
        # assuming that one record will be found in response.data
        meter = ComputeCompletion(response.data['results'])
        
        return JsonResponse(data={
            'profile_completed':meter.compute_percent(),
        })

"""class UpdateUserInfo( generics.UpdateAPIView ):
    # update user profile basic information in UserDetail Table
    # can update 3 table Auth_user, UserDetail or CandidateAttribute, not applicaable for clients, co-ordinators

    serializer_class = UserMeterSerializer
    queryset = UserDetail.objects.none()
    user_dict = {
        'user': ('first_name', 'last_name'),
        'userdetail': ('mobile', 'whatsapp_number', 'address', 'image', 'area', 'city', 'state'),
        'candidateattribute': ('language_proficiency', 'looks', 'open_to_which_kind_of_job', 'pay_scale', 'comfortable_travelling_outdoor', 'comfortable_for_liquor_promotion', 'comfortable_working_at_odd_timings', 'candidate_profile')
    }

    def put(self, request, *args, **kwargs):
        #    TABLE auth_user : first_name, last_name
        #    TABLE USERDETAIL : mobile, whatsapp_number, address, image, area, city, state
        #    TABLE CandidateAttribute : language_proficiency, looks, open_to_which_kind_of_job, pay_scale, comfortable_travelling_outdoor, comfortable_for_liquor_promotion, comfortable_working_at_odd_timings, candidate_profile

        user, userdetail, candidateattribute = {}, {}, {}
        # TODO change this to POST after integration
        kwargs.update(request.GET.dict())
        for model, keys in self.user_dict.items():
            for key in keys:
                if key in kwargs and kwargs[key] not in (None, ''):
                    eval("%s.update({ key:kwargs[key] })" % model)

        # TODO test this
        # update auth_user attributes
        User.objects.filter(id=request.user.id).update(**user)

        # update userdetails
        ud = UserDetail.objects.filter(auth_user=request.user)
        ud.update(**userdetail)

        # check if candidateattribute exists or not, create/update its attributes accordingly
        ca = CandidateAttribute.objects.filter(user=ud[0])
        if ca:
            ca.update(**candidateattribute)
        else:
            ca = CandidateAttribute.objects.create(**candidateattribute)
            ca.save()

        return JsonResponse(data={
            'status': True,
            'message': 'Profile Info Updated Successfully'
        })
"""

class UserProfileEvents( generics.ListAPIView, mygenerics.RelatedView ):
    """
    /my-profile/ page 
    get users event info

    """
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilters
    template_name = 'users/my_profile_base.html'

    def get_queryset(self, *args, **kwargs):
        if self.request._request.user:
            queryset = UserDetail.objects.filter(auth_user=self.request._request.user)
        else:
            queryset = UserDetail.objects.filter()
        return queryset

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(data={
                'status': False,
                'message': 'Unauthorized user, please login'
            })

        # view starts
        response = super(UserProfileEvents, self).get(request, *args, **kwargs)
        user_role = request.user.userdetail.type.slug 
        response.data['events'] = EventListing.as_data(serializer_class=ProfileEventSerializer)(request, userprofile=request.user.id, userrole=user_role)
            
        return response


from users.models import uploadpath
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='post')
class UserProfile( generics.ListAPIView, mygenerics.RelatedView ):
    serializer_class = UserMeterSerializer
    template_name = 'users/my_profile_base.html'
    related_views = {
        'state': (StateList.as_data(), '*', 1),
        'area': (AreaList.as_data(), '*', 1),
        'city': (CityList.as_data(), '*', 1),
    }

    def get_queryset(self, *args, **kwargs):
        if self.request._request.user:
            queryset = UserDetail.objects.filter(auth_user=self.request._request.user)
        else:
            queryset = UserDetail.objects.none()
        return queryset


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(data={
                'status': False,
                'message': 'Unauthorized user, please login'
            })
        
        response = super(UserProfile, self).get(request, *args, **kwargs)

        response.data['highest_qualification'] = HighestQualification.objects.all().values_list('slug', 'name')
        response.data['looks'] = LOOKS 
        response.data['language_proficiency'] = LANGUAGE_PROFICIENCY

        return response

    
    def post(self, request, *args, **kwargs):
        # shit: i wrote this function twice
        # from utility.fields import UserDetailFields, CandidateAttributeFields, ClientAttributeFields
        # update UserDetail
        # insert / update ClientAttribute / CandidateAttribute as per user type
        status = True
        message = "Successfully Updated."

        postdict = request.POST.dict()
        if postdict:

            authdict, userdict, attributedict = {}, {}, {}
            # prepare authuser table dictionary from postdata
            for f in AuthUserFields:
                if postdict.get(f):
                    authdict.update({
                        f: postdict.get(f)
                    })
            User.objects.filter(id=request.user.id).update(
                **authdict
            )

            # prepare userdetail table dictionary from postdata
            for f in UserDetailFields:
                if postdict.get(f):
                    userdict.update({
                        f: postdict.get(f)
                    })

            userdict.update({
                'area' : getobj(Area, userdict['area']),
                'city' : getobj(City, userdict['city']),
                'highest_qualification' : getobj(HighestQualification, userdict['highest_qualification'])
            })

            userdetail_instance = UserDetail.objects.filter(auth_user=request.user)

            profile_image = request.FILES.get('profile_image')
            if profile_image:
                
                handle_uploaded_file(profile_image, uploadpath(userdetail_instance[0], profile_image.name))
                userdict.update({
                    'image': uploadpath(userdetail_instance[0], profile_image.name)
                })


            # update userdetail table 
            userdetail_instance.update(
                **userdict
            )
            
            # similarly prepare client/candidate attributedict
            if request.user.userdetail.type.slug == 'client':
                whichattribute, whichattributefields = ClientAttribute, ClientAttributeFields
            elif request.user.userdetail.type.slug == 'candidate':
                whichattribute, whichattributefields = CandidateAttribute, CandidateAttributeFields
            else:
                whichattribute, whichattributefields = None, None
     

            for f in whichattributefields:
                if postdict.get(f):
                    attributedict.update({
                        f: postdict.get(f)
                    })

            # and update "type"attribute table if exists, else create it
            attr_obj = whichattribute.objects.filter(user__auth_user=request.user)
            if attr_obj:
                attr_obj.update(
                    **attributedict
                )
            else:
                attributedict.update({
                    'user': request.user.userdetail
                })
                whichattribute.objects.create(**attributedict)

        else:
            status = False
            message = "Nothing to update."

        return self.get(request, *args, **kwargs)



class UserProfileStats( generics.ListAPIView ):
    serializer_class = UserMeterSerializer
    template_name = 'users/my_profile_base.html'
    queryset = UserDetail.objects.none()

def handle_uploaded_file(f, d):
    with open(d, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
