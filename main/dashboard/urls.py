from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    # ------CATEGORY------------
    path('category-list/', views.category_list, name='category_list'),
    path('category-create/', views.category_create, name='category_create'),
    path('category-update/<int:id>/', views.category_update, name='category_update'),
    path('category-delete/<int:id>/', views.category_delete, name='category_delete'),
    # ------PRODUCT------------
    path('product-list/', views.product_list, name='product_list'),
    path('product-create/', views.product_create, name='product_create'),
    path('product-detail/<str:code>/', views.product_detail, name='product_detail'),
    path('product-update/<str:code>/', views.product_update, name='product_update'),
    path('product-delete/<str:code>/', views.product_delete, name='product_delete'),
    path('image-delete/<int:id>/', views.image_delete, name='image_delete'),
    path('video-delete/<int:id>/', views.video_delete, name='video_delete'),

    # ------EnterProduct--------
    path('enter-product-create/', views.enter_product_create, name='enter_product_create'),
    path('enter-product-list/', views.enter_product_list, name='enter_product_list'),
    path('enter-product-detail/<str:code>/', views.enter_product_history, name='enter_product_detail'),
    path('enter-product-update/<str:code>/', views.enter_product_update, name='enter_product_update'),



    path('profile_update/', views.profile_update, name='profile_update'),
    path('edit_password/', views.edit_password, name='edit_password'),
]