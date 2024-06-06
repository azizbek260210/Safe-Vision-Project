from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('log-out/', views.log_out, name='log-out'),

]