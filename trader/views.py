from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_protect

from rest_framework import routers, viewsets
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from rest_framework import status

from trader.models import UserProfile, Category, SaleItem
from trader.serializers import (CategorySerializer, UserProfileSerializer,
                                SaleItemSerializer)
from django.contrib.auth.models import User

import pdb

DEBUG = True

@api_view(['POST'])
def register_view(request):


    if request.method == 'POST':
        postdata = request.data
        # up_se = UserProfileSerializer
        username = postdata["username"]
        password = postdata["password"]
        email = postdata["email"]
        new_user = User.objects.create(username=username, password=password,
                                       email=email)
        new_user.save()
        new_user_id = new_user.id
        if DEBUG:
            return Response({"result":"created", "user_id": new_user_id}, status=status.HTTP_201_CREATED)
        return JsonResponse({"result":"created", "user_id": new_user_id})


@api_view(['POST'])
def login_view(request):

    if request.method == 'POST':
        postdata = request.data
        username = postdata["username"]
        password = postdata["password"]
        user_qs = User.objects.filter(username=username)
        if len(user_qs) == 0:
            return JsonResponse({"success": "false", "error": "no matched users",
                                 "user_id": None})
        if password != user_qs[0].password:
            return JsonResponse({"success": "false", "error": "wrong password",
                                 "user_id": None})
        user_id = user_qs[0].id
        if DEBUG:
            return Response({"success": "true", "user_id": user_id, "error": ""})
        return JsonResponse({"success": "true", "user_id": user_id, "error": ""})


@login_required
def my_account_view(request):
    template_name = "registration/my_account.html"
    page_title = _(u'My Account')
    users = UserProfile.objects.filter(user=request.user)
    name = request.user.username
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# @login_required
# def order_details_view(request, order_id, template_name="registration/order_details.html"):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     page_title = _(u'Order details for order #') + order_id
#     order_items = OrderItem.objects.filter(order=order)
#     return render_to_response(template_name, locals(),
#                               context_instance=RequestContext(request))


@login_required
def order_info_view(request, template_name="registration/order_info.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
    page_title = _(u'Edit Order Information')
    return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializers_class = UserProfileSerializer

def category_page(request):
    object_list = Category.objects.all()
    context = {'object_list': object_list,}
    return render(request, 'category_page.html', context)

ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', UserProfileViewSet)
ROUTER.register(r'categories', CategoryViewSet)




