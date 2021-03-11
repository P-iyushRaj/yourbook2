from django.urls import path
from .views import *
from . import views


app_name = 'app'

urlpatterns = [
    #path('', HomeView.as_view(), name='home'),you_seller
    path('', home , name='home'),
    path('search/', SearchPage, name='search_result'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('paymentcod/<payment_option>/', PaymentCOD.as_view(), name='payment-cod'),    

    path('products/', products, name='products'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile_edit/', views.update_profile, name='edit_profile'),

    path('you-seller/', you_seller , name='you-seller'),
    path('seller-register/', seller_register.as_view() , name='seller-register'),
    path('seller-account/', seller_account , name='seller-account'),
    path('sharing/', sharing, name='sharing'),
    path('renting/', renting, name='renting'),
    #path('seller-register/phone-verification/', phone_verification.as_view(), name='phone-verification'),
    path('phone-verification/', ValidatePhoneSendOTP.as_view(), name='phone-verification'),
    path('ValidateOTP/<slug>/', ValidateOTP.as_view(), name='ValidateOTP'),
    path('seller-details/', seller_details.as_view() , name='seller-details'),

    path('product/<slug>/', ItemDetailView, name='product'),
    path('add-to-cart/<slug>/', add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart,name='remove-from-cart'),

    path('increase-rent-time-interval/<slug>/', increase_rent_time_interval,name='increase-rent-time-interval'),
    path('reduce-rent-time-interval/<slug>/', reduce_rent_time_interval,name='reduce-rent-time-interval'),

    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('ordered-summary/', OrderedSummaryView.as_view(), name='ordered-summary'),
    path('share-summary/', ShareSummaryView.as_view(), name='share-summary'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),


    path('image_upload/', sharing, name = 'image_upload'), 
    path('success/', success, name = 'success'),
    #path('sharing/', AuthorCreate.as_view(), name = "sharing"),
    #path('distance/<slug>/', get_distance, name = 'get-distance'),

]

