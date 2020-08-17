from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.views import generic
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from Agents.models import PropertyUpload, Category, Available
from Services.models import RequestServices, ServiceType, Providers
from Payments.models import FundAccount, PromoteProperty
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
import datetime
from django.core.mail import send_mail
from django.db.models import Q

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user)
            messages.success(request, 'Profile successfully created')
            return redirect('accounts:auth_login')
    else:
        form = ProfileForm()
    return render(request, 'common/create_profile.html', {'form':form})

class ProfileSetUp(generic.DetailView):
    model = User
    template_name = 'common/initial_setup.html'


class UserProfile(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    model = Profile
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        pk = Profile.objects.get(pk=self.kwargs['pk'])
        property = PropertyUpload.objects.all().filter(created_by=pk)
        fund_acc = FundAccount.objects.all().filter(payee_id=pk)
        context = super(UserProfile, self).get_context_data(**kwargs)
        d = datetime.datetime.now()
        all_ads = PromoteProperty.objects.filter(promoter_id=pk)
        running_ads = PromoteProperty.objects.filter(Q(promoter_id=pk) & Q(expires__gte=d))
        if fund_acc:
            fund = FundAccount.objects.order_by('fundaccount__id').latest('new_balance')
            context['fund'] = fund
        if all_ads:
            context['all_ads'] = all_ads.count()
        context['count'] = property.count()
        context['running'] = running_ads.count()
        return context

def common(request):
    if request.user.profile:
        return redirect('common:profile', pk=request.user.profile.pk)

def direct(request):
    if request.user.has_perm('common.is_a_user'):
        return redirect('common:common')
    else:
        return redirect('common:initial', pk=request.user.pk)

class AvailableJobs(generic.DetailView):
    model = Profile
    template_name = 'common/available_jobs.html'

def availablejobs(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    provider = Providers.objects.get(provider_id=profile_id)
    type = ServiceType.objects.filter(service=provider.service_provided)
    requests = RequestServices.objects.filter(type_of_service=type)
    context_list = {'requests':requests}
    return render(request, 'common/available_jobs.html', context_list)

class ListServiceType(generic.DetailView):
    model = ServiceType
    template_name = 'common/service_professionals.html'

class ServiceProviderDetail(generic.DetailView):
    model = Providers
    template_name = 'common/service_provider_detail.html'


class AuthorUpdate(generic.UpdateView):
    model = Profile
    fields = ['name']
    template_name_suffix = '_update_form'

def send_msg(request):
    name = request.POST.get('name')
    msg = request.POST.get('msg')
    subject = request.POST.get('subject')
    email = request.POST.get('mail')
    data = {'name':name, 'msg':msg, 'subject':subject, 'email':email}
    if data:
        message = "%s: %s via %s" % (name, msg, email)
        send_mail(subject, message, 'EasyEstate.com.ng <noreply@easyestate.com.ng>', ['mailing.accomodo@gmail.com'])
        messages.success(request, 'Message sent')
    return redirect('index')

def about(request):
    return render(request, 'common/about_us.html')