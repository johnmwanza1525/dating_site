from django.shortcuts import render,redirect,get_object_or_404
import uuid
import logging
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
import string
from .utils import send_verification_email as send_verification_email2# Ensure this utility function is correctly defined
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import requests
from django.http import JsonResponse
from django.utils import timezone
from .models import EmailVerificationToken

# Create your views here.
def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_verification_email2(request, user, email)
            messages.success(request, "Password reset email has been sent.")
        except User.DoesNotExist:
            messages.warning(request, "No user is associated with this email address.")
        return redirect('user_password_reset')
    return render(request, 'password/password_reset.html')

def reset_password_confirm(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        email_token = get_object_or_404(EmailVerificationToken, user=user, token=token)

        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                email_token.is_verified = True
                email_token.save()
                messages.success(request, "Password reset successful. You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")

        if not email_token.is_verified:
            return render(request, 'password/reset_password_confirm.html', {'validlink': True})

        messages.error(request, "Invalid or expired password reset link.")
        return redirect('password_reset')

    except (User.DoesNotExist, EmailVerificationToken.DoesNotExist):
        messages.error(request, "Invalid password reset link.")
        return redirect('password_reset')
