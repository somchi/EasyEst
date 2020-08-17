from .models import Category, PriceRange, PropertyUpload
from Payments.models import PromoteProperty, PromotionCategories
from django.db.models import Q
from state.models import State
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def PropertyCategory(request):
    cat = Category.objects.all()
    cat_context = {'cat': cat}
    return cat_context

def PropertyMaxPrice(request):
    max_price = PriceRange.objects.all()
    max_context = {'max_price': max_price}
    return max_context

def PromotedProperties(request):
    date = datetime.datetime.now()
    page = request.GET.get('page', 1)
    visibility = PromotionCategories.objects.filter(class_of_transaction='Featured')
    property = PromoteProperty.objects.filter(Q(visibility_point__in=visibility) & Q(expires__gte=date))
    paginator = Paginator(property, 5)
    try:
        properties = paginator.get_page(page)
    except PageNotAnInteger:
        properties = paginator.get_page(1)
    except EmptyPage:
        properties = paginator.get_page(paginator.num_pages)
    context = {'properties':properties}
    return context

def Properties(request):
    property = PropertyUpload.objects.filter(status='Approved')
    property_list = {'property': property}
    return property_list

def listed_pro(request):
    listed = PropertyUpload.objects.all()
    list = {'listed':listed}
    return list

def state(request):
    state = State.objects.all()
    state_list = {'state':state}
    return state_list
