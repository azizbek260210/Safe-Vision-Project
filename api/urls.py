from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list),
    path('wishlist/', views.wishlist),

    path('log_in/', views.log_in),
    path('code_confirm/', views.code_confirm),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete_profile'),
]