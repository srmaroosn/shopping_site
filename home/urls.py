
from django import views
from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItems, name='update_item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('logout/', views.user_logout, name='logout')
]
