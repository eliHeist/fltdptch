from django import forms
from django.contrib.auth import get_user_model, forms as auth_forms
from django.contrib.auth.models import Permission

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


User = get_user_model()

class PasswordResetForm(auth_forms.PasswordResetForm):
    pass


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    def save(self, request=None, custom_message=None, domain="app.terekaonline.com", reset_type="reset", **kwargs):
        protocol = "http"
        if settings.DEBUG:
            domain = "localhost:8000"
            protocol = "http"
        if request:
            domain = get_current_site(request).domain
            if request.is_secure():
                protocol = "https"
            
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': 'FLTDSPTCH',
                'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
                'custom_message': custom_message,  # 👈 my custom context
                'reset_type': "reset"
            }

            subject = "Password Reset on FLTDSPTCH" if reset_type == "reset" else "Set up your FLTDSPTCH password"
            body = render_to_string('registration/password_reset_email_message.html', context)
            html_email = render_to_string('registration/password_reset_email.html', context)

            email_message = EmailMultiAlternatives(subject, body, kwargs.get('from_email'), [user.email])
            email_message.attach_alternative(html_email, "text/html")
            email_message.send()

