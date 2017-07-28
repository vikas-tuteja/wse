from django.conf.urls import url

from users.views import CreateUser, LoginUser, ChangePassword, ForgotPassword, CheckUsernameExists, UserProfileCompletionMeter, UserProfile


urlpatterns = [
    url(r'^create-user/$', CreateUser.as_view(), name="create_user"),
    url(r'^login/$', LoginUser.as_view(), name="login"),
    url(r'^forgot-password/$', ForgotPassword.as_view(), name="forgot_password"),
    url(r'^change-password/$', ChangePassword.as_view(), name="change_password"),
    url(r'^user-exists/$', CheckUsernameExists.as_view(), name="user_exists"),
    url(r'^user-meter/$', UserProfileCompletionMeter.as_view(), name="user_meter"),
    url(r'^my-profile/$', UserProfile.as_view(), name="my_profile"),
]
