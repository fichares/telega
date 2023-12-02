from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView, ListView, TemplateView, UpdateView
from mail_templated import EmailMessage

from chat.forms import ForgetPasswordUser, LoginForm, RegistrationForm
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
                return redirect("general_chat")
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
            return redirect('general_chat')
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
                message = EmailMessage('chat/reset_pasword_email.tpl', {'user': self.request.user, 'domain': current_site,'token': token, 'uid': uid}, settings.EMAIL_HOST_USER, [current_user.email])
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
    template_name = 'chat/update_password.html'







class GeneralChatMixin(TemplateView):
    template_name = "chat/GENERAL_chat.html"

    def get_context_data(self, **kwargs):
        current_user = User.objects.get(username='admin')
        current_user.quotation = 'edadsad'
        print(current_user.quotation)






