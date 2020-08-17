from django.shortcuts import render, get_object_or_404, redirect
from common.models import Profile
from django.views import generic
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MessageProviderForm, EmailSellerForm
from Services.models import Providers
from django.http import JsonResponse
from Agents.models import PropertyUpload, Category
from .models import MessageProvider, EmailSeller,  Chart
import datetime
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

@login_required
def messageprovider(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)
    sender = get_object_or_404(Profile, pk=request.user.profile.pk)
    receiver = get_object_or_404(Providers, provider_id=profile)
    full_name = request.POST.get('full_name')
    subject = request.POST.get('email_subject')
    message = request.POST.get('message')
    phone = request.POST.get('phone')
    data = {'sender':sender, 'receiver':receiver, 'sender_name':full_name,'message':message, 'message_subject':subject, 'phone':phone}
    f = MessageProviderForm(data)
    if f.is_valid() and f.clean():
        email = MessageProvider.objects.create(sender=sender, receiver=receiver, sender_name=full_name,message=message,
                                message_subject=subject, phone=phone, date_created=datetime.datetime.now, read='False')
        send_mail(subject, "Sender's Details: {}, {}. \n {}".format(sender.user.email, phone, message), 'EasyEstate.com.ng <noreply@easyestate.com.ng>', [receiver.provider.user.email])
    else:
        messages.warning(request, 'There is an error in your submission {}'.format(f.errors))
        return redirect('common:provider_detail', receiver.pk)
    messages.success(request, 'Email delivered successfully to {}. Thanks {} for your interest'.format(receiver.full_name.capitalize(), full_name))
    return redirect('common:provider_detail', receiver.pk)

class MessageProviderDetail(generic.DetailView):
    model = Profile
    template_name = 'message/messages.html'

def chat(request, user_id):
    user = get_object_or_404(Profile, pk=user_id)
    chart = Chart.objects.all()
    return render(request, 'message/chat.html', {'chart':chart})

def post(request):
    if request.method =="POST":
        msg = request.POST.get("msgbox", None)
        c = Chart(user=request.user.profile, message=msg)
        if msg != "":
            c.save()
        return JsonResponse({'msg':msg, 'user':c.user.username})

def emailseller(request, property_id):
    property = get_object_or_404(PropertyUpload, pk=property_id)
    full_name = request.POST.get('full_name')
    subject = request.POST.get('email_subject')
    message = request.POST.get('message')
    from_email = request.POST.get('email_address')
    phone = request.POST.get('phone')
    data = {'property':property, 'receiver':property.created_by_id, 'your_name':full_name, 'email_address':from_email,
            'message':message, 'subject':subject, 'contact_no':phone}
    f = EmailSellerForm(data)
    if f.is_valid() and f.clean():
        email = EmailSeller.objects.create(property=property, receiver=property.created_by, your_name=full_name,
        email_address=from_email, message=message, subject=subject, contact_no=phone)
        send_mail(subject, "Sender's Details: {}, {}. \n {}".format(from_email, phone, message), 'EasyEstate.com.ng <noreply@easyestate.com.ng>', [property.created_by.user.email])
    else:
        messages.warning(request, 'There is an error in your submission')
        return redirect('agents:property_detail', property.pk)
    messages.success(request, "Email delivered successfully to {}. Thanks {} for your interest. Seller's Contact: {}".format(property.created_by.user.username.capitalize(), full_name, property.created_by.phone_number))
    return redirect('agents:property_detail', property.pk)

def mail_suggestion(request, sender_id):
    sender = get_object_or_404(Profile, pk=sender_id)
    if request.method == 'POST':
        level = request.POST.get('level')
        suggestion = request.POST.get('suggestion')
        category = request.POST.get('category')
        message = "Sender's Details: {}, {}.\n Category:{}.\n Level: {}.\n {}".format(sender.user.email, sender.phone_number, category, level, suggestion)
        send_mail("Feature Suggestions", message, 'EasyEstate.com.ng <noreply@easyestate.com.ng>', ['mailing.easyestate@gmail.com', 'chisomike11@gmail.com'])
    return redirect('common:profile', sender.pk)





