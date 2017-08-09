from django.conf.urls import url

from users.views import CreateUser, LoginUser, ChangePassword, ForgotPassword, CheckUsernameExists, UserProfileCompletionMeter, UserProfile, UpdateUserInfo, Logout

urlpatterns = [
    url(r'^create-user/$', CreateUser.as_view(), name="create_user"),
    url(r'^login/$', LoginUser.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),
    url(r'^forgot-password/$', ForgotPassword.as_view(), name="forgot_password"),
    url(r'^change-password/$', ChangePassword.as_view(), name="change_password"),
    url(r'^user-exists/$', CheckUsernameExists.as_view(), name="user_exists"),
    url(r'^user-meter/$', UserProfileCompletionMeter.as_view(), name="user_meter"),
    url(r'^update-info/$', UpdateUserInfo.as_view(), name="update_info"),


    # my profile page
    url(r'^my-profile/$', UserProfile.as_view(), name="my_profile"),
    url(r'^my-profile/overview/$', UserProfile.as_view(), name="my_overview"),  
    url(r'^my-profile/profile/$', UserProfile.as_view(), name="my_profile"),    
    url(r'^my-profile/notification/$', UserProfile.as_view(), name="my_notify"),    
    url(r'^my-profile/stats/$', UserProfile.as_view(), name="my_stat"),
]
