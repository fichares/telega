{% extends "chat/reset_password_user_class.tpl" %}

{% block subject %}
Hello {{user.username}}
{% endblock %}

{% block body %}
To initiate the password reset process for your Account {{ user.email }},
click the link below:

http://{{ domain }}{% url 'reset_password' uidb64=uid token=token %}

If clicking the link above doesn't work, please copy and paste the URL in a new browser
window instead.
{% endblock %}