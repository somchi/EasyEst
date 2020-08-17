from django.db import models
from common.models import Profile
from decimal import Decimal as D
from django.db.models import Sum
import datetime
from decimal import Decimal
import math
import random
from Services.models import RequestInterest
import hmac
from Agents.models import PropertyUpload
from django.conf import settings

#This model is used to fund account
class FundAccount(models.Model):
    payee = models.ForeignKey(Profile)
    amount = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    old_balance = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    new_balance = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    reference = models.CharField(max_length=64, unique=True)
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.amount:
            p = Profile.objects.get(pk=self.payee_id)
            self.old_balance = FundAccount.objects.filter(payee_id=p).aggregate(Sum('amount')).get('amount__sum') or 0
            self.new_balance = Decimal(self.old_balance) + Decimal(self.amount or 0)
        super(FundAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.payee.user.username


#This model handles all the debit transactions made on fund
class DebitsTrasactions(models.Model):
    profile = models.ForeignKey(Profile)
    available_fund = models.ForeignKey(FundAccount)
    reference = models.CharField(max_length=64, unique=True, null=True)
    transaction_cost = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    balance = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.reference

#This model categorize promotion
class PromotionCategories(models.Model):
    class_of_transaction = models.CharField(max_length=50)
    transaction_cost = models.DecimalField(max_digits=50, decimal_places=0, default=0)

    def __str__(self):
        return self.class_of_transaction

#This model handles all property promotions
class PromoteProperty(models.Model):
    property = models.ForeignKey(PropertyUpload)
    promoter = models.ForeignKey(Profile)
    visibility_point = models.ForeignKey(PromotionCategories)
    transaction_ref = models.CharField(max_length=64, unique=True)
    date_created = models.DateField(auto_now_add=True)
    expires = models.DateTimeField()

    class Meta:
        ordering = ('date_created','visibility_point')
    
    def save(self):
        date = datetime.timedelta(days=10)
        if not self.id:
            self.expires = datetime.datetime.now() + date
            super(PromoteProperty, self).save()
        self.transaction_ref = math.floor((random.random() * 10000000000) + 1)
        super(PromoteProperty, self).save()

    def __str__(self):
        return self.transaction_ref

#This model handle all the earnings of a providers
class ProviderIncome(models.Model):
    payee = models.ForeignKey(Profile)
    amount = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    old_balance = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    new_balance = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    reference = models.CharField(max_length=64, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Awaiting Clearance")

    def save(self, *args, **kwargs):
        if self.amount:
            p = Profile.objects.get(pk=self.payee_id)
            self.old_balance =ProviderIncome.objects.filter(payee_id=p).aggregate(Sum('amount')).get('amount__sum') or 0
            self.new_balance = Decimal(self.old_balance) + Decimal(self.amount or 0)
        super(ProviderIncome, self).save(*args, **kwargs)

    def __str__(self):
        return self.payee.user.username

#This model allow a person pay for a custom offer he/she created to the person his/she granted's it to.
class PayForCustomRequest(models.Model):
    payer = models.ForeignKey(Profile)
    request_interest = models.ForeignKey(RequestInterest)
    transaction_cost = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    order_id = models.CharField(max_length=64, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_earned = models.DecimalField(max_digits=50, decimal_places=0, default=0)

    def save(self, *args, **kwargs):
        self.order_id = math.floor((random.random() * 10000000000) + 1)
        percentage = Decimal(self.transaction_cost) * 10 / 100
        self.amount_earned = Decimal(self.transaction_cost - percentage)
        super(PayForCustomRequest, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id










