from django.urls import path

from chat.views import FeedbackWithAdmin, ForgetPasswordUser, GeneralChat, LogoutUsersFromSistem, MainPageNoAuurization, \
    RessetPassword, \
    login_user, \
    register_user

#from . import views

urlpatterns = [
    path('', MainPageNoAuurization.as_view(), name='mainpage'),
    path('login', login_user, name='login'),
    path('registration', register_user, name='registration'),
    path('forget_password', ForgetPasswordUser.as_view(), name='forget_password'),
    path('chats/<str:room_name>', GeneralChat.as_view(), name='general_chat'),
    path('password-reset/<str:uidb64>/<str:token>/<slug:idx>', RessetPassword.as_view(), name='reset_password'),
    path('logout', LogoutUsersFromSistem, name='logout'),
    path('feedback', FeedbackWithAdmin.as_view(), name='feedback'),
]