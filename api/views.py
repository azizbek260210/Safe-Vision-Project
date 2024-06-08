from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from main import models
from . import serializers


@api_view(['GET',])
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
