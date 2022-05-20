
from django import views
from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItems, name='update_item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
