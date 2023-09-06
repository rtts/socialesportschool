from django.urls import reverse
from django.utils import timezone
from django.template import Template, Context
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from registration.backends.hmac.views import RegistrationView, ActivationView
from .models import *
from .forms import *
from bootcamps.models import *

def testpage(request, slug='meedoen'):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    icons = SocialMedia.objects.all()
    footer = Config.objects.filter(parameter__in=[1,2,3])
    sort = request.GET.get('sort', 'date')

    bootcamps = Bootcamp.objects.filter(date__gte=timezone.now().date(), deleted=False)
    if sort == 'date':
        bootcamps = bootcamps.order_by('date', 'start_time')
    elif sort == 'city':
        bootcamps = sorted(bootcamps, key=lambda x: x.get_city())

    return render(request, 'testpage.html', {
        'page': page,
        'pages': pages,
        'sections': sections,
        'footer': footer,
        'icons': icons,
        'bootcamps': bootcamps,
        'sort': sort,
    })

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    icons = SocialMedia.objects.all()
    footer = Config.objects.filter(parameter__in=[1,2,3])
    sort = request.GET.get('sort', 'date')

    bootcamps = Bootcamp.objects.filter(date__gte=timezone.now().date(), deleted=False)
    if sort == 'date':
        bootcamps = bootcamps.order_by('date', 'start_time')
    elif sort == 'city':
        bootcamps = sorted(bootcamps, key=lambda x: x.get_city())

    return render(request, 'page.html', {
        'page': page,
        'pages': pages,
        'sections': sections,
        'footer': footer,
        'icons': icons,
        'bootcamps': bootcamps,
        'sort': sort,
    })

def terms(request):
    try:
        terms = Config.objects.get(parameter=34).content
    except Config.DoesNotExist:
        terms = ''
    return render(request, 'terms.html', {
        'terms': terms,
    })

class Login(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=20).content
        except Config.DoesNotExist:
            pass
        return context

class Logout(LogoutView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=21).content
        except Config.DoesNotExist:
            pass
        return context

class Register(RegistrationView):
    form_class = RegistrationForm
    template_name = 'aanmelden.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=10).content
        except Config.DoesNotExist:
            pass
        return context

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user,
            'voornaam': user.first_name,
            'achternaam': user.last_name,
            'activatielink': 'http://' + context['site'].domain + reverse('registration_activate', args=[context['activation_key']]),
        })

        try:
            email_subject_template = Template(Config.objects.get(parameter=12).content)
        except Config.DoesNotExist:
            email_subject_template = Template('')
        try:
            email_body_template = Template(Config.objects.get(parameter=13).content)
        except Config.DoesNotExist:
            email_body_template = Template('')

        subject = email_subject_template.render(Context(context))
        subject = ''.join(subject.splitlines())
        message = email_body_template.render(Context(context))

        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

class Activate(ActivationView):
    template_name = 'registration/activation_failed.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=15).content
        except Config.DoesNotExist:
            pass
        return context

def thanks(request):
    try:
        message = Config.objects.get(parameter=11).content
    except Config.DoesNotExist:
        message = ''
    return render(request, 'registration/thanks.html', {
        'message': message,
    })

def success(request):
    try:
        message = Config.objects.get(parameter=14).content
    except Config.DoesNotExist:
        message = ''
    return render(request, 'registration/success.html', {
        'message': message,
    })

class PasswordReset(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=30).content
        except Config.DoesNotExist:
            pass
        return context

class PasswordResetDone(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=31).content
        except Config.DoesNotExist:
            pass
        return context

class PasswordResetConfirm(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=32).content
        except Config.DoesNotExist:
            pass
        return context

class PasswordResetComplete(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['message'] = Config.objects.get(parameter=33).content
        except Config.DoesNotExist:
            pass
        return context

