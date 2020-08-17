from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from .forms import PropertyUploadForm, PropertyUpdateForm
from Payments.models import FundAccount, PromoteProperty
from Payments.forms import PromotePropertyForm
from .models import PropertyUpload, Category
from common.models import Profile
from state.models import LGA, State
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
import json
import datetime
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse

def propertyupload(request, user_id):
    created_by = get_object_or_404(Profile, pk=user_id)
    if request.method == "POST":
        form = PropertyUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(created_by)
            messages.success(request, 'Property uploaded successfully')
            send_mail('Approval Request', 'You have a property awaiting approval', 'EasyEstate.com.ng <noreply@easyestate.com.ng>', ['chisomike11@gmail.com'])
            return redirect('common:profile', created_by.pk)
    else:
        form = PropertyUploadForm()
    return render(request, 'agents/property_upload.html', {'form':form})



class UserProperties(generic.DetailView):
    model = Profile
    template_name = 'agents/user_properties.html'

    def get_context_data(self, **kwargs):
        pk = Profile.objects.get(pk=self.kwargs['pk'])
        property = PropertyUpload.objects.filter(created_by_id=pk)
        context = super(UserProperties, self).get_context_data(**kwargs)
        for e in property:
            d = datetime.datetime.now()
            #t = e.date_created
            status = PropertyUpload.objects.filter(running='Running', date_expire__lte=d).update(running='Expired')
            #status2 = PropertyUpload.objects.filter(Q(running='Expired') & Q(date_created=t)).update(running='Running')
            context['status'] = status
            return context

class UserAds(generic.DetailView):
    model = Profile
    template_name = 'agents/user_ads.html'

    def get_context_data(self, **kwargs):
        pk = Profile.objects.get(pk=self.kwargs['pk'])
        person = PropertyUpload.objects.filter(created_by_id=pk)
        context = super(UserAds, self).get_context_data(**kwargs)
        d = datetime.datetime.now()
        status = PromoteProperty.objects.filter(Q(promoter_id=pk) & Q(expires__gte=d))
        context['running'] = status.count()
        return context


def deleteproperty(request, request_id):
    obj = get_object_or_404(PropertyUpload, pk=request_id)
    if request.method == "POST":
        parent_url = obj.created_by.get_absolute_url()
        obj.delete()
        messages.success(request, "Item deleted")
        return HttpResponseRedirect(parent_url)
    return render(request, 'agents/confirm_property_delete.html', {'object':obj})

class PropertyUpdate(generic.UpdateView):
    model = PropertyUpload
    form_class = PropertyUpdateForm
    template_name = 'agents/property_update_form.html'

    def get_success_url(self):
        return reverse('agents:user_properties', kwargs={'pk': self.request.user.profile.pk})

def promoteproperty(request, property_id):
    property = get_object_or_404(PropertyUpload, pk=property_id)
    promoter = property.created_by_id
    profile = get_object_or_404(Profile, pk=promoter)
    promoter_fund = FundAccount.objects.filter(payee_id=promoter)
    if request.method=='POST':
        form = PromotePropertyForm(request.POST)
        for available_fund in promoter_fund:
            if form.is_valid() and form.cleaned_data['visibility_point'].transaction_cost < available_fund.new_balance:
                available_fund.new_balance = available_fund.new_balance - form.cleaned_data['visibility_point'].transaction_cost
                FundAccount.objects.filter(payee_id=profile).update(new_balance=available_fund.new_balance)
                form.save(property, profile)
                messages.success(request, 'Ad promotion started')
                redirect('agents:user_properties', profile.pk)
            else:
                messages.success(request, 'You are low on fund')
    else:
        form = PromotePropertyForm()
    return render(request, 'agents/promote_property.html', {'form':form})

def findproperty(request, ):
    if request.method == 'GET':
        where_in_state = request.GET.get('lga')
        state = request.GET.get('state')
        price_max = request.GET.get('price_max')
        property_type = request.GET.get('property_type')
        p = LGA.objects.filter(name__icontains=where_in_state)
        s = State.objects.get(name__icontains=state)
        t = Category.objects.get(name__icontains=property_type)
        result = PropertyUpload.objects.filter(Q(status='Approved'), Q(property_type=t) | Q(property_lga=p) | Q(property_state=s) | Q(price__lte=price_max))
        return render(request, 'agents/result.html', {'result': result})
    else:
        return render(request, 'agents/result.html', {})

def ajax_lga_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        nigerian_state = request.GET.get('nigerian_state', '')
        state =State.objects.filter(name__icontains=nigerian_state)
        lgas = LGA.objects.filter(state=state, name__icontains=q)
        results = []
        for pl in lgas:
            lgas_json = {}
            lgas_json['id'] = pl.id
            lgas_json['label'] = pl.name
            lgas_json['value'] = pl.name
            results.append(lgas_json)
        data = json.dumps(list(results), cls=DjangoJSONEncoder)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ajax_state_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        states = State.objects.filter(name__icontains=q)
        results = []
        for pl in states:
            states_json = {}
            states_json['id'] = pl.id
            states_json['label'] = pl.name
            states_json['value'] = pl.name
            results.append(states_json)
        data = json.dumps(list(results), cls=DjangoJSONEncoder)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

class PropertyDetail(generic.DetailView):
    model = PropertyUpload
    template_name = 'agents/property_detail.html'



