from django.conf.urls import url

from users.views import CreateUser, LoginUser, ChangePassword
urlpatterns = [
    url(r'^create-user/$', CreateUser.as_view()),
    url(r'^login/$', LoginUser.as_view()),
    url(r'^change-password/(?P<user_email>[-\w]+)/$', ChangePassword.as_view()),
]
