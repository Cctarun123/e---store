from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('orders/', views.order_history, name='order_history'),
    path('profile/', views.profile, name='profile'),
]
