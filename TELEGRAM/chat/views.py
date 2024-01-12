from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView, ListView, TemplateView, UpdateView
from mail_templated import EmailMessage

from chat.forms import EnterMessageChat, ForgetPasswordUser, LoginForm, RegistrationForm
from chat.models import Chat_Application, MessageUser, Users_Chat
from chat.utils import DataMixin
from user_app.models import User

message_not_found_email = 'The mail was not found.'
message_sen_instructions_your_email = 'The instructions send your email.'
current_site = '127.0.0.1:8000'                     ###

class MainPageNoAuurization(TemplateView):
    template_name = 'chat/MainPageNoAuurization.html'


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                user.online = True
                user.save()
                login(request, user)
                return redirect("general_chat", room_name='general_chat')
            else:
                messages.error(request, 'Check your login details and try again',
                               extra_tags='alert alert-danger alert-dismissible fade show'
                              )
    return render(request, "chat/login_form.html", {"form": form})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration was successful',
                             extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('general_chat', room_name='general_chat')
    else:
        form = RegistrationForm()
    return render(request, 'chat/registration_form.html', {'form': form})



class ForgetPasswordUser(FormView):
    template_name = 'chat/forget_password.html'
    form_class = ForgetPasswordUser


    def form_valid(self, form):
        email = form.data['email_reset']
        print(email)

        try:
            current_user = User.objects.get(email=email)
            token = default_token_generator.make_token(current_user)
            uid = urlsafe_base64_encode(force_bytes(current_user.pk))
            try:
                print(current_site, uid, token)
                message = EmailMessage('chat/reset_pasword_email.tpl', {'user': self.request.user, 'domain': current_site,'token': token, 'uid': uid, 'id': current_user.id}, settings.EMAIL_HOST_USER, [current_user.email])
                message.send()
                print('Good')
            except:
                print('Error')

            messages.success(self.request, message_sen_instructions_your_email)
            return redirect(self.request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            messages.error(self.request, message_not_found_email)
            return redirect(self.request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))



class RessetPassword(UpdateView):
    model = User
    fields = ["password"]
    template_name = 'chat/update_password.html'


    def get_object(self):
        object = get_object_or_404(User, id=self.kwargs['idx'])
        return object

    def form_valid(self, form):
        now_password = form.cleaned_data.get('password')
        now_user = self.get_object()
        print(now_user)
        user = User.objects.get(id=self.kwargs['idx'])
        user.password = now_password
        user.save()
     #   now_user.update(password=now_password)
      #  authenticate(now_user, now_password)
        return redirect('general_chat', room_name='general_chat')



class GeneralChat(DataMixin, TemplateView, FormView):
    template_name = "chat/GENERAL_chat.html"
    form_class = EnterMessageChat

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        name_chat = Chat_Application.objects.get(name_chat='General Chat')
        messagge_chat = MessageUser.objects.filter(chat_it_is=name_chat).order_by('data_create')
        data['messages'] = messagge_chat
        data['room_name'] = "general-chat"
        current_user = User.objects.get(username='admin')
        print('1')
        return data

    def get_data_to_templates(self ):
        pass

    def form_valid(self, form):
        message  = form.cleaned_data['enter_chat']
        chat_name =  self.kwargs['room_name']
        if chat_name == 'general_chat':
            chat_name = 'General Chat'
        chat = Chat_Application.objects.get(name_chat=chat_name)
        MessageUser.objects.create(text=message, users_send=self.request.user, chat_it_is=chat)
        print(form.cleaned_data)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class My_chat(DataMixin, TemplateView):
    template_name = 'chat/my_chats.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user_chats = Users_Chat.objects.filter(users=self.request.user)
        message_chats = []
        for e in user_chats:
            message_chats.append(MessageUser.objects.filter(chat_it_is=e.chat).last())
        print(user_chats)
        print(message_chats)
        data['user_chats'] = user_chats
        data['message_chats'] = message_chats
        data['now_time'] = datetime.now()
        # last_messages_chats =
        return data


def LogoutUsersFromSistem(request):
    pass


class FeedbackWithAdmin(CreateView):
    pass






