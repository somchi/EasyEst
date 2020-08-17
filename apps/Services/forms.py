from django import forms
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import Providers, RequestServices, RequestInterest, ProviderBuild

# form to create service profile
class ProviderForm(forms.ModelForm):
    class Meta:
        model = Providers
        exclude = ('provider', 'date_joined', )
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_provided': forms.Select(attrs={'class': 'form-control'}),
            'since': forms.DateInput(attrs={'class': 'form-control', 'id':'datepicker'}),
            'major_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'major_jobs_done': forms.Textarea(attrs={'class': 'form-control'}),
            'to': forms.DateInput(attrs={'class': 'form-control'}),
            'service_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'starting_at': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your least charge'}),

        }

    def save(self, user):
        provider = super(ProviderForm, self).save(commit=False)
        provider.provider = user
        provider.save()

# form to create a service request
class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestServices
        exclude = ('requester', 'status', 'date_approved', 'date_created', 'provider_granted')
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_service': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'price_from': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_to': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, requester):
        user = super(RequestServiceForm, self).save(commit=False)
        user.requester = requester
        user.save()


class RequestInterestsForm(forms.ModelForm):
    class Meta:
        model = RequestInterest
        exclude = ('interested_person', 'request', 'approved','status', 'due_date', )
        widgets = {
            'my_offer': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_offer': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, request_id, person_id):
        person = super(RequestInterestsForm, self).save(commit=False)
        person.interested_person = person_id
        person.request = request_id
        person.save()


class RequestServicesEditForm(forms.ModelForm):
    class Meta:
        model = RequestServices
        fields = ('type_of_service', 'job_title', 'duration', 'price_from', 'price_to')
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_service': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'price_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'N'}),
            'price_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'N'}),
        }

class ProfileBuildForm(forms.ModelForm):
    class Meta:
        model = ProviderBuild
        exclude = ('provider', )
        widgets = {
            'certificate_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_acquired':forms.DateInput(attrs={'class': 'form-control', 'id':'datepicker'}),
            'issuer':forms.TextInput(attrs={'class':'form-control'}),
            'cert_evidence':forms.FileInput(attrs={'class':'form-control'})
        }

    def save(self, user):
        pro = super(ProfileBuildForm, self).save(commit=False)
        pro.provider = user
        pro.save()
        try:
            pro.provider = user
        except pro.DoesNotExist:
            raise Http404("Poll does not exist")
        pro.save()