import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import EmailVerificationToken

def send_verification_email(request, user, email):
    token = uuid.uuid4()
    EmailVerificationToken.objects.update_or_create(user=user, defaults={'token': token, 'is_verified': False})

    reset_url = request.build_absolute_uri(
        reverse('reset_password_confirm', kwargs={'user_id': user.pk, 'token': token})
    )

    subject = 'Password Reset Request'
    message = f'Hi {user.username},\n\nTo reset your password, click the link below:\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
