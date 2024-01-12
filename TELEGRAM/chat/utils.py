from .models import *

shapka_for_chat_verx =  [
        {'title': "about", 'url_name': 'about'},
        {'title': "push", 'url_name': 'push_notification'},
        {'title': "Feedback", 'url_name': 'feedback'},
        {'title': "Logout", 'url_name': 'logout'},
        {'title': "name_company", 'url_name': 'NetWorkinn'}
]

menu_for_chat_verx =  [
        {'title': "Profile", 'url_name': 'profile'},
        {'title': "Friends", 'url_name': 'friends'},
        {'title': "Chats", 'url_name': 'my_chats'},
        {'title': "Photo", 'url_name': 'photo'},
        {'title': "Files", 'url_name': 'files'},
        {'title': "Reminder", 'url_name': 'reminder'},
        {'title': "News", 'url_name': 'news'},
        {'title': "Games", 'url_name': 'games'},
        {'title': "Helpes", 'url_name': 'helpes'},
]

class DataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['a'] = 'adnin-top'
        context['logo'] = shapka_for_chat_verx
        context['menu'] = menu_for_chat_verx
        return context
