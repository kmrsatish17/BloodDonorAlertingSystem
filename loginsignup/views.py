from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import logging

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ipware.ip import get_ip

from loginsignup.forms import RegistrationForm, EditProfileForm
from loginsignup.tokens import account_activation_token

logger = logging.getLogger(__name__)


# Create your views here.

# use generic views

def home(request):
    return render(request, 'loginsignup/index.html', {})


def confirmation(request):
    return render(request, 'loginsignup/confirmation.html', {})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # takes the post data from request
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.refresh_from_db()
            user.donor.blood_group = form.cleaned_data.get('blood_group')
            user.donor.phone = form.cleaned_data.get('phone')
            user.donor.city = form.cleaned_data.get('city')
            user.donor.state = form.cleaned_data.get('state')
            user.donor.country = form.cleaned_data.get('country')
            user.save()
            user.donor.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Blood-e-Merry Account'
            message = render_to_string('loginsignup/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, from_email='visesh@bloodemerry.com')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return HttpResponseRedirect(reverse('loginsignup:confirmation'))
        else:
            logger.error('Form invalid')
            return render(request, 'loginsignup/signup.html', {'form': form, 'error_message': "Form data invalid!", })
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # # if user is not None:
            # login(request, user)

    else:
        form = RegistrationForm()
        return render(request, 'loginsignup/signup.html', {'form': form})


def profile(request):
    args = {'user': request.user}
    client_address = get_ip(request)
    logger.error('ip=' + client_address)
    return render(request, 'loginsignup/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)  # takes the post data from request
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.donor.blood_group = form.cleaned_data.get('blood_group')
            user.donor.phone = form.cleaned_data.get('phone')
            user.donor.city = form.cleaned_data.get('city')
            user.donor.state = form.cleaned_data.get('state')
            user.donor.country = form.cleaned_data.get('country')
            user.save()
            user.donor.save()
            return HttpResponseRedirect(reverse('loginsignup:profile'))
        else:
            logger.error('Form invalid')
            return render(request, 'loginsignup/edit_profile.html', {'form': form, 'error_message': "Form data invalid!", })

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'loginsignup/edit_profile.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.donor.email_confirmed = True
        user.save()
        user.donor.save()
        login(request, user)
        return render(request, 'loginsignup/index.html', {})
    else:
        return render(request, 'loginsignup/account_activation_invalid.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)  # takes the post data from request
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('loginsignup:profile'))
        else:
            logger.error('Form invalid')
            return render(request, 'loginsignup/change_password.html', {'form': form, 'error_message': "Form data invalid!", })

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'loginsignup/change_password.html', {'form': form})
