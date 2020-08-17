from django import forms
from .models import FundAccount, PromoteProperty, PayForCustomRequest

class FundAccountForm(forms.ModelForm):
    class Meta:
        model = FundAccount
        exclude = ('payee', 'old_balance', 'new_balance' , 'reference')
        widgets = {
            "amount": forms.NumberInput(attrs={'class': 'form-control', 'id':'amount'}),
        }

    def save(self, payee_id):
        payee = super(FundAccountForm, self).save(commit=False)
        payee.payee = payee_id
        payee.save()

class PromotePropertyForm(forms.ModelForm):
    class Meta:
        model = PromoteProperty
        exclude = ('property', 'promoter', 'expires', 'transaction_ref', )
    def save(self, property, promoter):
        promotor = super(PromotePropertyForm, self).save(commit=False)
        promotor.property = property
        promotor.promoter = promoter
        promotor.save()

class PayForCustomRequestForm(forms.ModelForm):
    class Meta:
        model = PayForCustomRequest
        exclude = ('payer', 'request_interest', 'amount_earned', )
    def save(self, payer, request_interest):
        pay = super(PayForCustomRequestForm, self).save(commit=False)
        pay.payer = payer
        pay.request_interest = request_interest