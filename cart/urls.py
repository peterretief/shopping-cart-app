from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.VegetableListView.as_view(), name='vegetable_list'),
    
    # Cart URLs
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:veg_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:veg_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:veg_id>/', views.update_quantity, name='update_quantity'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('summary/', views.vegetable_order_summary, name='vegetable_summary'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
]
