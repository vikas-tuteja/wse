from django.conf.urls import url

from users.views import CreateUser, LoginUser, ChangePassword, ForgotPassword, CheckUsernameExists


urlpatterns = [
    url(r'^create-user/$', CreateUser.as_view()),
    url(r'^login/$', LoginUser.as_view()),
    url(r'^forgot-password/$', ForgotPassword.as_view()),
    url(r'^change-password/$', ChangePassword.as_view()),
    url(r'^user-exists/$', CheckUsernameExists.as_view()),
]
