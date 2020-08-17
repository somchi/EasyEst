from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
import datetime
from django.core.mail import send_mail
from Services.models import RequestInterest, RequestServices, Providers
from .forms import FundAccountForm, PayForCustomRequestForm
from common.models import Profile
from django.contrib import messages
from .models import FundAccount, PayForCustomRequest, ProviderIncome

def fund(request, payee_id):
    payee = get_object_or_404(Profile, pk=payee_id)
    cash = FundAccount.objects.filter(payee_id=payee_id)
    return render(request, 'payments/finance.html', {'payee':payee})

# This view interact with paystack to credit a users account
def fundaccount(request):
    payee = request.user.profile
    if request.is_ajax() and request.method =="POST":
        amount = request.POST.get('amount')
        reference = request.POST['ref']
        f = FundAccount.objects.create(payee=payee, amount=amount, reference=reference)
        status = "Good"
        return HttpResponse(status)
    else:
        status="Bad"
        return HttpResponse(status)


def custompaysummary(request, id):
    request_interest = get_object_or_404(RequestInterest, pk=id)
    context = {'request_interest':request_interest}
    return render(request, 'payments/checkout_custom_request.html', context)

#to be used when we start collecting payments
'''def payforcustomrequest(request, id):
    request_interest = get_object_or_404(RequestInterest, pk=id)
    p = Providers.objects.get(pk=request_interest.interested_person_id)
    r = Profile.objects.get(pk=p.provider_id)
    req = RequestServices.objects.get(pk=request_interest.request_id)
    t = Profile.objects.get(pk=req.requester_id)
    payer_fund = FundAccount.objects.filter(payee_id=t)
    if payer_fund:
        for available_fund in payer_fund:
            if request_interest.price_offer < available_fund.new_balance:
                payment = PayForCustomRequest.objects.create(payer=t, request_interest=request_interest, transaction_cost=request_interest.price_offer)
                income = ProviderIncome.objects.create(payee=r, amount=payment.amount_earned, reference=payment.order_id)
                available_fund.new_balance = available_fund.new_balance - request_interest.price_offer
                FundAccount.objects.filter(payee_id=t).update(new_balance=available_fund.new_balance)
                date = datetime.timedelta(days=request_interest.duration)
                time = datetime.datetime.now() + date
                interest = RequestInterest.objects.filter(pk=id).update(status='Granted')
                due_date = RequestInterest.objects.filter(pk=id).update(due_date=time)
                email = send_mail('Request Approval', "your offer '{}' has been granted".format(request_interest.my_offer), t.user.email,
                                  [p.provider.user.email])
    else:
        messages.success(request, 'You are low on fund')
        return redirect('payments:fund_account', t.pk)
    messages.success(request, 'Payment Successful')
    return redirect('payments:fund_account', t.pk)'''




