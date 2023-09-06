from django.template import Template, Context
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from sss.utils import get_config
from .models import *
from .forms import *

def participate(request, pk):
    bootcamp = get_object_or_404(Bootcamp, pk=pk)
    if request.POST:
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.bootcamp = bootcamp
            participant.save()

            subject = get_config(60)
            message = Template(get_config(61))
            context = Context({
                'voornaam': participant.name,
                'datum': bootcamp.date,
                'tijd': bootcamp.start_time,
                'adres': bootcamp.get_location(),
            })
            email = EmailMessage(subject, message.render(context), settings.DEFAULT_FROM_EMAIL, [participant.email], reply_to=[bootcamp.user.email])
            #email.send()

            return render(request, 'registration/thanks.html', {
                'message': get_config(50),
            })

    else:
        form = ParticipantForm()
    return render(request, 'participate.html', {
        'message': get_config(49),
        'bootcamp': bootcamp,
        'form': form,
    })

@login_required
def participants(request, pk):
    bootcamp = get_object_or_404(Bootcamp, pk=pk)
    (orgs, current_org) = get_orgs(request)
    return render(request, 'participants.html', {
        'bootcamp': bootcamp,
        'current_org': current_org,
    })

@login_required
def participant(request, pk):
    bootcamp = get_object_or_404(Bootcamp, pk=pk)
    (orgs, current_org) = get_orgs(request)
    if request.POST:
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.bootcamp = bootcamp
            participant.save()

            response = redirect('participants', bootcamp.pk)
            response['Location'] += '?org={}'.format(current_org.rank)
            return response
    else:
        form = ParticipantForm()

    return render(request, 'participant.html', {
        'current_org': current_org,
        'bootcamp': bootcamp,
        'form': form,
    })

@login_required
def delete_participant(request, pk):
    (orgs, current_org) = get_orgs(request)
    p = get_object_or_404(Participant, pk=pk)
    bootcamp = p.bootcamp

    if isinstance(current_org, ZorgLocatie) and bootcamp.zorglocatie != current_org:
        return HttpResponseForbidden('You don’t have permission to delete this participant')
    if isinstance(current_org, Sportschool) and bootcamp.sportschool != current_org:
        return HttpResponseForbidden('You don’t have permission to delete this participant')

    p.delete()

    response = redirect('participants', bootcamp.pk)
    response['Location'] += '?org={}'.format(current_org.rank)
    return response

def get_orgs(request):
    try:
        org = int(request.GET.get('org', '1'))
    except ValueError:
        org = 1
    zorglocaties = list(request.user.zorglocaties.all())
    sportscholen = list(request.user.sportscholen.all())
    orgs = zorglocaties + sportscholen

    try:
        current_org = orgs[org-1]
    except IndexError:
        return ([], None)

    current_org.rank = org
    return (orgs, current_org)

@login_required
def bootcamps(request):
    (orgs, current_org) = get_orgs(request)

    if not orgs:
        return render(request, 'payday.html', {})

    if isinstance(current_org, ZorgLocatie):
        bootcamps = Bootcamp.objects.filter(zorglocatie=current_org, deleted=False)
        caregiver = True
    elif isinstance(current_org, Sportschool):
        bootcamps = Bootcamp.objects.filter(sportschool=current_org, deleted=False)
        caregiver = False

    return render(request, 'bootcamps.html', {
        'orgs': orgs,
        'current_org': current_org,
        'bootcamps': bootcamps,
        'caregiver': caregiver,
    })

@login_required
def bootcamp(request, pk=None):
    (orgs, current_org) = get_orgs(request)

    if pk:
        bootcamp = get_object_or_404(Bootcamp, pk=pk)
        if isinstance(current_org, ZorgLocatie) and bootcamp.zorglocatie != current_org:
            return HttpResponseForbidden('You don’t have permission to edit this bootcamp')
        if isinstance(current_org, Sportschool) and bootcamp.sportschool != current_org:
            return HttpResponseForbidden('You don’t have permission to edit this bootcamp')
    else:
        bootcamp = None

    if request.POST:
        form = BootcampForm(request.POST, instance=bootcamp, org=current_org)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user
            b.save()
            response = redirect('bootcamps')
            response['Location'] += '?org={}'.format(current_org.rank)
            return response
    else:
        form = BootcampForm(instance=bootcamp, org=current_org)

    return render(request, 'bootcamp.html', {
        'add': not bool(bootcamp),
        'form': form,
        'current_org': current_org,
    })

@login_required
def delete_bootcamp(request, pk):
    (orgs, current_org) = get_orgs(request)
    bootcamp = get_object_or_404(Bootcamp, pk=pk)

    if isinstance(current_org, ZorgLocatie) and bootcamp.zorglocatie != current_org:
        return HttpResponseForbidden('You don’t have permission to delete this bootcamp')
    if isinstance(current_org, Sportschool) and bootcamp.sportschool != current_org:
        return HttpResponseForbidden('You don’t have permission to delete this bootcamp')

    bootcamp.deleted = True
    bootcamp.save()
    response = redirect('bootcamps')
    response['Location'] += '?org={}'.format(current_org.rank)
    return response

@login_required
def change_org(request, org):
    zorglocaties = list(request.user.zorglocaties.all())
    sportscholen = list(request.user.sportscholen.all())
    orgs = zorglocaties + sportscholen

    try:
        current_org = orgs[int(org)-1]
        current_org.rank = org
    except:
        raise Http404

    if isinstance(current_org, ZorgLocatie):
        Form = ZorgLocatieForm
        org_type = 'Zorgorganisatie'
    elif isinstance(current_org, Sportschool):
        Form = SportschoolForm
        org_type = 'Sportclub'

    if request.POST:
        form = Form(request.POST, request.FILES, instance=current_org)
        if form.is_valid():
            form.save()
            response = redirect('bootcamps')
            response['Location'] += '?org={}'.format(current_org.rank)
            return response
    else:
        form = Form(instance=current_org)

    return render(request, 'change_org.html', {
        'current_org': current_org,
        'org_type': org_type,
        'form': form,
    })

@login_required
def pay(request, orgtype=None):
    if orgtype == 'zorg':
        Form = ZorgLocatieForm
        try:
            price = Price.objects.get(product=1)
        except Price.DoesNotExist:
            price = 0
        message = get_config(40)

    elif orgtype == 'sport':
        Form = SportschoolForm
        try:
            price = Price.objects.get(product=2)
        except Price.DoesNotExist:
            price = 0
        message = get_config(41)
    else:
        raise NotImplementedError()

    if request.POST:
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            org = form.save()
            now = timezone.now()
            invoice = Invoice(
                identifier = org.name.replace(' ','').upper() + str(now.year),
                date = now,
                amount = price.amount,
                description = price.description,
                user = request.user,
                )
            org.users.add(request.user)
            if orgtype == 'zorg':
                invoice.zorglocatie = org
            if orgtype == 'sport':
                invoice.sportschool = org
            invoice.save()

            try:
                send_mail(
                    'SSS: NIEUWE FACTUUR',
                    'Er is een nieuwe factuur beschikbaar op www.socialesportschool.nl' + invoice.get_absolute_url(),
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                )
            except:
                pass

            return redirect('invoice', invoice.pk)
    else:
        form = Form()

    return render(request, 'pay.html', {
        'orgtype': orgtype,
        'form': form,
        'message': message,
        'extra_message': get_config(42),
    })

@login_required
def invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if invoice.user != request.user and not request.user.is_staff:
        raise Http404
    if invoice.zorglocatie:
        org = invoice.zorglocatie
    elif invoice.sportschool:
        org = invoice.sportschool
    else:
        raise Http404

    # Security bolted on:
    if not request.user.is_staff:
        (orgs, current_org) = get_orgs(request)
        if org not in orgs:
            raise Http404

    subtotal = float(invoice.amount)
    vat = 0.21 * subtotal
    total = 1.21 * subtotal

    return render(request, 'invoice.html', {
        'org': org,
        'invoice': invoice,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
    })
