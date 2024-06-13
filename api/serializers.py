from rest_framework.serializers import ModelSerializer
from main import models



class UserListSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name', ]


class SubCategoryListSerializer(ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ['id', 'name', 'image']


class CategoryListSerializer(ModelSerializer):
    sub_category = SubCategoryListSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'sub_category']


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
    category = SubCategoryListSerializer()

    class Meta:
        model = models.Product
        fields = ['id', 'category', 'name', 'des', 'des2', 'price', 'quantity', 'images']
        depth = 1


class WishListSerializer(ModelSerializer):
    product = ProductListSerializer()
    user = UserListSerializer()

    class Meta:
        model = models.WishList
        fields = ['id', 'user', 'product']
        depth = 1
