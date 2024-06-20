from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login, logout

from main import models
from . import serializers
from random import randint
from twilio.rest import Client
import re


@api_view(['GET', ])
def product_list(request):
    products = models.Product.objects.all()
    categorys = models.Category.objects.all()
    banners = models.Banner.objects.all()
    product_serializer = serializers.ProductListSerializer(products, many=True)
    category_serializer = serializers.CategoryListSerializer(categorys, many=True)
    banner_serializer = serializers.BannerListSerializer(banners, many=True)
    return Response(
        {
            'categorys': category_serializer.data,
            'banner': banner_serializer.data,
            'products': product_serializer.data,

        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET', ])
def wishlist(request):
    wishlist = models.WishList.objects.filter(user=request.user)
    wishlist_serializer = serializers.WishListSerializer(wishlist, many=True)
    return Response(
        {
            'wishlist': wishlist_serializer.data,
        },
        status=status.HTTP_200_OK,
    )


# ------------------Auth -------------------------

def send_sms(body, number):
    account_sid = 'AC791d8890b344f107c15a6ca74f2a8119'
    auth_token = 'd133e5bb7f001c0535eda53056a06065'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_='+14325274551',
        to=number
    )
    return message


@api_view(['GET', 'POST'])
def log_in(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        # if not re.match(r'^\+?\d{11}$', phone):
        #     return Response({"error": "Invalid phone number format."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = models.CustomUser.objects.get_or_create(phone=phone)
        confirm = user.confirm = randint(10000, 99999)
        user.save()
        send_sms("Sizning tasdiqlash kodingiz: " + str(confirm), user.phone)

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
    return Response({"message": "Verification code error."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def code_confirm(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        confirm = request.POST.get('code')
        try:
            user = models.CustomUser.objects.get(phone=phone)
            if user.verify_code(confirm):
                user.is_active = True
                user.confirm = None
                user.save()
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                if user.first_name and user.last_name:
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                return Response({"token": token.key, "message": "Profile incomplete."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except models.CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Verification code error."}, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserProfileSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
