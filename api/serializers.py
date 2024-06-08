from rest_framework.serializers import ModelSerializer
from main import models


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name']


class BannerListSerializer(ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ['id', 'img', ]


class ImageListSerializer(ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['img', ]


class ProductListSerializer(ModelSerializer):
    images = ImageListSerializer(many=True)
    class Meta:
        model = models.Product
        fields = ['id', 'category', 'name', 'des', 'des2', 'price', 'quantity', 'images']
        depth = 1