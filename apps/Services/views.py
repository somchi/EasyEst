from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import generic
from state.models import LGA, State
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.models import Profile
from django.db.models import Q
from django.core.mail import send_mail
import datetime
from django.core.urlresolvers import reverse
from .forms import ProviderForm, RequestServiceForm, RequestInterestsForm, RequestServicesEditForm, ProfileBuildForm
from .models import Providers, RequestServices, RequestInterest, ServiceType
from django.contrib import messages


# function to create a service profile
def provider(request, user_id):
    pro = get_object_or_404(Profile, pk=user_id)
    if request.method == "POST":
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save(pro)
            messages.success(request, 'Profile creation successful')
            return redirect('service:manage_service', pro.pk)
    else:
        form = ProviderForm()
    return render(request, 'services/create_profile.html', {'form': form})

# class that handles users service section (Manage Service)
class ManageService(generic.DetailView):
    model = Profile
    template_name = 'services/manage_service.html'

    # fetch's the service the user renders, if any
    def get_context_data(self, **kwargs):
        pk = Profile.objects.get(pk=self.kwargs['pk'])
        provider = Providers.objects.all().filter(provider_id=pk)
        req = RequestServices.objects.all().filter(requester_id=pk)
        g = RequestInterest.objects.filter(Q(interested_person_id=provider) & Q(status='Granted'))
        context = super(ManageService, self).get_context_data(**kwargs)
        if provider:
            pro = Providers.objects.select_related('service_provided').get(provider_id=pk)
            type = ServiceType.objects.filter(service=pro.service_provided)
            jobs = RequestServices.objects.filter(type_of_service=type)
            p = pro.service_provided
            context['provider'] = p
            context['jobs'] = jobs.count()
        if g:
            context['offered'] = g.count()
        context['requester'] = req.count()
        return context

def requestservice(request, requester_id):
    requester = get_object_or_404(Profile, pk=requester_id)
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            form.save(requester)
            messages.success(request, 'Request successfully created')
            return redirect('service:my_requests', requester.pk)
    else:
        form = RequestServiceForm()
    return render(request, 'services/custom_request.html', {'form': form})

def requestinterests(request, request_id):
    req = get_object_or_404(RequestServices, pk=request_id)
    provider = request.user.profile.providers
    if request.method == 'POST':
        form = RequestInterestsForm(request.POST)
        if form.is_valid():
            form.save(req, provider)
            messages.success(request, 'Offer Sent')
            return redirect('service:my_requests', request.user.profile.pk)
    else:
        form = RequestInterestsForm()
    return render(request, 'services/send_proposal.html', {'form':form})

class MyRequest(generic.DetailView):
    model = Profile
    template_name = 'services/custom_requests.html'
    def get_context_data(self,  **kwargs):
        pk = Profile.objects.get(pk=self.kwargs['pk'])
        provider = Providers.objects.all().filter(provider_id=pk)
        sent_request = RequestInterest.objects.all().filter(interested_person_id=provider)
        req = RequestServices.objects.all().filter(requester_id=pk)
        g = RequestInterest.objects.filter(Q(interested_person_id=provider) & Q(status='Granted'))
        d = datetime.datetime.now()
        due = RequestInterest.objects.filter(due_date__lte=d).update(status='Completed')
        context = super(MyRequest, self).get_context_data(**kwargs)
        if sent_request:
            context['jobs'] = sent_request.count()
        if req:
            context['requester'] = req.count()
        if g:
            context['offered'] = g.count()
        return context

def deleterequest(request, request_id):
    obj = get_object_or_404(RequestServices, pk=request_id)
    if request.method == "POST":
        parent_url = obj.requester.get_absolute_url()
        obj.delete()
        messages.success(request, "Item deleted")
        return HttpResponseRedirect(parent_url)
    return render(request, 'services/request_services_confirm_delete.html', {'object':obj})

class RequestServicesEdit(generic.UpdateView):
    model = RequestServices
    form_class = RequestServicesEditForm
    template_name = 'services/request_services_edit.html'

    def get_success_url(self):
        return reverse('service:my_requests', kwargs={'pk': self.request.user.profile.pk})

def buildprofile(request, provider_id):
    profile = Profile.objects.get(pk=provider_id)
    provider = Providers.objects.get(provider_id=profile)
    if request.method == "POST":
        form = ProfileBuildForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(provider)
            messages.success(request, 'Added successfully')
            return redirect('service:manage_service', profile.pk)
    else:
        form = ProfileBuildForm()
    return render(request, 'services/build_profile.html', {'form': form})


def approverequest(request, id):
    p = RequestInterest.objects.get(pk=id)
    req = RequestServices.objects.get(pk=p.request_id)
    t = Profile.objects.get(pk=req.requester_id)
    i = Providers.objects.get(pk=p.interested_person_id)
    date = datetime.timedelta(days=p.duration)
    time = datetime.datetime.now() + date
    interest = RequestInterest.objects.filter(pk=id).update(status='Granted')
    due_date = RequestInterest.objects.filter(pk=id).update(due_date=time)
    email = send_mail('Request Approval', "your offer '{}' has been granted".format(p.my_offer),
                      'EasyEstate.com.ng < noreply @ easyestate.com.ng>',
                      [i.provider.user.email])
    messages.success(request, 'You have granted {} the job. \n Job Due Date is: {}'.format(i.full_name, p.due_date))
    return redirect('service:my_requests', t.pk)

def findprovider(request):
    page = request.GET.get('page', 1)
    where_in_state = request.GET.get('lga')
    state = request.GET.get('state')
    service_type = request.GET.get('service_type')
    p = LGA.objects.get(name__icontains=where_in_state)
    s = State.objects.get(name__icontains=state)
    r = Providers.objects.filter(service_provided=service_type)
    t = Profile.objects.filter(Q(lga=p) & Q(state=s))
    results = Providers.objects.filter(Q(provider=t) | Q(service_provided=service_type))
    paginator = Paginator(results, 3)
    try:
        sult = paginator.page(page)
    except PageNotAnInteger:
        sult = paginator.page(1)
    except EmptyPage:
        sult = paginator.page(paginator.num_pages)
    return render(request, 'services/result.html', {'sult':sult})



