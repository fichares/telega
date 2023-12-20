from django.urls import path

from user_app.views import ChatsUsers, FilesUsers, FriendsUsers, GamesUsers, HelpersUsers, NewsUsers, PhotosUsers, \
    ProfileUsersR, \
    Profile_users, \
    PushNotifUsers, ReminderUsers

urlpatterns = [
    path('profile', Profile_users.as_view(), name='profile_users'),
    path('push', PushNotifUsers.as_view(), name='push_users'),
    path('profile', ProfileUsersR.as_view(), name='profile'),
    path('friends', FriendsUsers.as_view(), name='friends'),
    path('chats', ChatsUsers.as_view(), name='chats'),
    path('photo', PhotosUsers.as_view(), name='photo'),
    path('files', FilesUsers.as_view(), name='files'),
    path('reminder', ReminderUsers.as_view(), name='reminder'),
    path('news', NewsUsers.as_view(), name='news'),
    path('games', GamesUsers.as_view(), name='games'),
    path('helpes', HelpersUsers.as_view(), name='helpes'),

]