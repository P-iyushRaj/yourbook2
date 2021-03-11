from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance

# Create your views here.
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView,View
from django.utils import timezone

from django.http import HttpResponse 
from .forms import *
from django.db import transaction
from django.utils.translation import gettext as _
from django.conf import settings

from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.views import APIView
from rest_framework.response import Response

def view_profile(request):

    destination,l_lat, l_lon = get_destination(request)

    return render(request, "profile.html", { 'destination':destination })

@login_required
@transaction.atomic
def update_profile(request):
    #profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('app:view_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    destination,l_lat, l_lon = get_destination(request)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'destination':destination,
    })

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        destination,l_lat, l_lon = get_destination(self.request)
        context = {
            'form': form,
            'destination' : destination,
        }
        return render(self.request, "checkout-page.html", context)

    def post(self, *args, **kwargs):
        
        form = CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                phone = form.cleaned_data.get('phone')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    phone = phone,
                    country = country,
                    zip = zip,
                    payment_option = payment_option
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option=='S':
                    return redirect("app:payment", payment_option = 'Stripe')
                elif payment_option=='COD':
                    return redirect("app:payment-cod", payment_option = 'cod')
                    
                else :
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect("app:checkout")
            
            else:
                messages.warning(self.request, "check the options correctly")
                return redirect("app:checkout")
                

        except ObjectDoesNotExist:
            messages.error(self.request, "You donot have active order")
            return redirect("app:order-summary")


import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
  #"sk_test_4eC39HqLyjWDarjtT1zdp7dc"

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
class PaymentCOD(LoginRequiredMixin, View):
    def get(self, *args, **kwargs ):
        order = Order.objects.get(user = self.request.user, ordered =False)
        order.ordered = True
        order.save()
        messages.success(self.request, "Your order is successful")
        return redirect('/')

class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        destination,l_lat, l_lon = get_destination(self.request)
        return render(self.request, "payment.html", { 'destination':destination})

    def post(self, *args, **kwargs):
        order = Order.objects.get(  user = self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount=int(order.get_total())

        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount= amount,
                currency="usd",
                source=token
            )
            #payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.amount = order.get_total()
            payment.user = self.request.user
            payment.save()

            #assign payment to the order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order is successful")
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.err('error', {})
            messages.error(self.request, f"{error.get('message')}")
            return redirect('/')

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "RateLimitError")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "InvalidRequestError")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "AuthenticationError")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network error")
            return redirect('/')

        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong, you were not charged.Try again")
            return redirect('/')

        except Exception as e:
            messages.error(self.request, "A serious error occured. We have been notified")
            return redirect('/')

class seller_register(LoginRequiredMixin, View):  
    def get(self, *args, **kwargs):
            form = SellerRegisterForm()
            destination,l_lat, l_lon = get_destination(self.request)
            context = {
                'form': form,
                'destination' : destination,
            }
            return render(self.request, "selleraccount/seller_register.html", context)

    def post(self, *args, **kwargs):
        
        form = SellerRegisterForm(self.request.POST or None)
        try:
            if form.is_valid():
                companyName = form.cleaned_data.get('companyName')
                terms_condition = form.cleaned_data.get('terms_condition')
                #condition if the user already resistered
                try :
                    Seller_user = SellerProfile.objects.get( user = self.request.user)
                    messages.error(self.request, "you are already registered")
                    return redirect("app:seller-account")
                #a user can create many seller profile
                except:
                    Seller_Profile = SellerProfile(                            
                        user = self.request.user,
                        companyName = companyName,
                        terms_condition = terms_condition,
                    )
                    Seller_Profile.save()
                    return redirect("app:phone-verification")
            else:
                messages.error(self.request, "fill the correct fields")
                return redirect("app:seller-register")
                
        except ObjectDoesNotExist:
            messages.error(self.request, "fill the required fields")
            return redirect("")

@login_required
def you_seller(request):
    #if not registered
    destination,l_lat, l_lon = get_destination(request)
    #Seller_user = SellerProfile.objects.get( user = request.user)
    context = {
                'destination':destination,
            }
    try :
        Seller_user = SellerProfile.objects.get( user = request.user)
        return redirect("app:seller-account")
    except: 
        return render(request, "selleraccount/you_sell.html", context= context)

@login_required
def seller_account(request):
    destination,l_lat, l_lon = get_destination(request)
    items = Item.objects.all()[0:10]
    
    context = {
            'destination':destination,
            'items' : items,
        }
    return render(request, "selleraccount/seller_profile.html", context= context)
    #return redirect("app:phone-verification")

import requests
def send_otp(phone):
    if phone:
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
        result = requests.get(link, verify=False)
        return otp_key
    else:
        return False

def send_otp_forgot(phone):
    if phone:
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        user = get_object_or_404(user=self.request.user.userprofile, phone__iexact = phone)
        if user.name:
            name = user.name
        else:
            name = phone
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfgs&templatename=Wisfrags&var1={name}&var2={otp_key}'
        #result = requests.get(link, verify=False)
        #print(result)      
        return otp_key
    else:
        return False

class ValidatePhoneSendOTP(LoginRequiredMixin, APIView):

    def get(self, *args, **kwargs):
        form = mobileverification()
        destination,l_lat, l_lon = get_destination(self.request)
        context = {
            'form': form,
            'destination' : destination,
            'button' : 'Send OTP',
        }
        return render(self.request, "selleraccount/phone_verify.html", context)

    def post(self, request, *args, **kwargs):
        form = mobileverification(self.request.POST or None)
    
        if form.is_valid():
            phone = str(form.cleaned_data.get('phone'))
            user = SellerProfile.objects.filter(phone__iexact = phone)
            if user.exists():
                messages.error(self.request, "Phone Number already exists")
                return redirect("app:phone-verification")
                # return Response({'status': False, 'detail': 'Phone Number already exists'})
                # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                #print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    #print(old)
                    if old.exists():
                        old_qs = old[0]
                        count = old_qs.count
                        old_qs.count += 1
                        #increase count and add otp
                        old_qs.otp = otp
                        old_qs.save()
                    else:
                        count = count + 1
                        PhoneOTP.objects.create(
                            phone =  phone, 
                            otp =   otp,
                            count = count
        
                            )
                    if count > 20:
                        #return Response({
                        #     'status' : False, 
                        #     'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        # })
                        messages.error(self.request, "Maximum otp limits reached. Kindly support our customer care or try with different number")
                        return redirect("app:phone-verification")
                else:
                    # return Response({
                    #             'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                    #         })
                    messages.error(self.request, "OTP sending error. Please try after some time.")
                    return redirect("app:phone-verification")

                # return Response({
                #     'status': True, 'detail': 'Otp has been sent successfully.'
                # })
                messages.success(self.request, "Otp has been sent successfully." + phone)
                return redirect("app:ValidateOTP" , slug = phone)
        else:
            # return Response({
            #     'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            # })
            messages.error(self.request, "I haven't received any phone number. Please do a POST request.")
            return redirect("app:phone-verification")

                
                #a user can't create many seller profile
            #     Seller_user = SellerProfile.objects.get( user = self.request.user)
            #     Seller_user.phone = phone
            #     Seller_user.save()
            #     return redirect("app:ValidateOTP")
            # else:

            #     messages.error(self.request, "fill the correct phone number")
            #     return redirect("app:phone-verification")

        
'''
class ValidatePhoneSendOTP(APIView):
    
    #This class view takes phone number and if it doesn't exists already then it sends otp for
    #first coming phone numbers

    def get(self, *args, **kwargs):
        form = ValidatePhoneSendOTPform()
        Seller_Profile = SellerProfile.objects.get( user = self.request.user)
        
        phone_number = Seller_Profile.__class__.objects.values('phone')
        number = phone_number[0].get('phone')
        #print(phone_number)
        #print(phone_number[0].get('phone'))
        destination,l_lat, l_lon = get_destination(self.request)
        context = {
            'form': form,
            'destination' : destination,
            'phone_number' : number,
            'button' : 'Submit OTP' ,
        }
        return render(self.request, "selleraccount/phone_verify.html", context)

    def post(self, request, *args, **kwargs):
        Seller_Profile = SellerProfile.objects.get( user = self.request.user)
        phone_number = Seller_Profile.objects.values('phone')
        if phone_number:
            phone = str(phone_number)
            User=self.request.user.userprofile
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            })

class ValidateOTP(APIView):

    def get(self, *args, **kwargs):
        form = ValidatePhoneSendOTPform()
        destination,l_lat, l_lon = get_destination(self.request)
        context = {
            'form': form,
            'destination' : destination,
            'button' : 'Verify OTP',
        }
        return render(self.request, "selleraccount/phone_verify.html", context)


    def post(self, request, *args, **kwargs):
        form = ValidatePhoneSendOTPform(self.request.POST or None)
    
        if form.is_valid():
            #phone = request.data.get('phone', False)
            #otp_sent   = request.data.get('otp', False)
            print(phone, otp_sent)

            if phone and otp_sent:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    otp = old.otp
                    if str(otp) == str(otp_sent):
                        old.logged = True
                        old.save()

                        return Response({
                            'status' : True, 
                            'detail' : 'OTP matched, kindly proceed to save password'
                        })
                    else:
                        return Response({
                            'status' : False, 
                            'detail' : 'OTP incorrect, please try again'
                        })
                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                    })


            else:
                return Response({
                    'status' : 'False',
                    'detail' : 'Either phone or otp was not recieved in Post request'
                })

'''

class ValidateOTP(LoginRequiredMixin, APIView):

    def get(self, *args, **kwargs):
        form = ValidatePhoneSendOTPform()
        destination,l_lat, l_lon = get_destination(self.request)
        context = {
            'form': form,
            'destination' : destination,
            'button' : 'Verify OTP',
        }
        return render(self.request, "selleraccount/phone_verify.html", context)

    def post(self, request, *args, **kwargs):
        form = ValidatePhoneSendOTPform(self.request.POST or None)
        phone = str(kwargs['slug'])
        if form.is_valid():
            #phone = request.data.get('phone', False)
            #otp_sent   = request.data.get('otp', False)
            #need phone no. here / SENT OTP
            otp_sent = form.cleaned_data.get('otp')
            #print(otp_sent, kwargs)
            
            if phone and otp_sent:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old_qs = old[0]
                    #old_qs = old_qs.first()
                    otp = old_qs.otp
                    if str(otp) == str(otp_sent):
                        old_qs.logged = True
                        old_qs.save()

                        Seller_Profile = SellerProfile.objects.get( user = self.request.user )
                        Seller_Profile.phone = phone
                        Seller_Profile.verified = True
                        Seller_Profile.save()

                        messages.error(self.request, "OTP matched phone verified, kindly proceed")
                        return redirect("app:seller-details")
                
                    else:
                        messages.error(self.request, "OTP incorrect, please try again")
                        return redirect("app:ValidateOTP" , slug = phone)
                else:
                    messages.error(self.request, "Phone not recognised. Kindly request a new otp with this number")
                    return redirect("app:phone-verification")

            else:
                messages.error(self.request, "Either phone or otp was not recieved in Post request")
                return redirect("app:phone-verification")
        else:
            messages.error(self.request, "I haven't received any OTP. Please do a POST request.")
            return redirect("app:phone-verification")

class seller_details(LoginRequiredMixin, View):  
    def get(self, *args, **kwargs):
            form = SellerRegisterForm()
            destination,l_lat, l_lon = get_destination(self.request)
            context = {
                #'form': form,
                'destination' : destination,
            }
            return render(self.request, "selleraccount/Seller_Details.html", context)

    def post(self, *args, **kwargs):
        
        form = SellerRegisterForm(self.request.POST or None)
        try:
            if form.is_valid():
                companyName = form.cleaned_data.get('companyName')
                terms_condition = form.cleaned_data.get('terms_condition')
                #condition if the user already resistered
                try :
                    Seller_user = SellerProfile.objects.get( user = self.request.user)
                    messages.error(self.request, "you are already registered")
                    return redirect("app:seller-account")
                #a user can create many seller profile
                except:
                    Seller_Profile = SellerProfile(                            
                        user = self.request.user,
                        companyName = companyName,
                        terms_condition = terms_condition,
                    )
                    Seller_Profile.save()
                    return redirect("app:phone-verification")
            else:
                messages.error(self.request, "fill the correct fields")
                return redirect("app:seller-register")
                
        except ObjectDoesNotExist:
            messages.error(self.request, "fill the required fields")
            return redirect("")


#geopy, geoip2, maxmind database city+country
from geopy.extra.rate_limiter import RateLimiter
from .utils import *
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

@login_required
def sharing(request): 
    if request.method == 'POST': 
        form = ShareForm(request.POST, request.FILES)
        #formA = ShareFormA(request.POST, request.FILES)
        geolocator = Nominatim(user_agent= 'app' )

        if form.is_valid():
            form.instance.user = request.user
            #form.instance.created_by = request.user
            destination_ = form.cleaned_data.get('zip_code')
            try:
                destination = geolocator.geocode(destination_)
                #print(destination)
                d_lat = int(destination.latitude)
                d_lon = int(destination.longitude)
                # form.instance.lat = d_lat
                # form.instance.lon = d_lon
                form.instance.location = Point(d_lon, d_lat,srid=4326)
                #location = Point(d_lon, d_lat,srid=4326)
                #print(location)
                form.instance.Item_type = 'Sell'
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, "Book shared successfully")
                return redirect('/')
            except:
                messages.error(request, "Inter a valid Zip Code")
                pass
            
    else: 
        form = ShareForm()
        
    destination,l_lat, l_lon = get_destination(request)

    return render(request, 'productin-page.html', {'form' : form, 'formtype' : 'Book Seling form' ,'destination':destination})
    
def success(request): 
    return HttpResponse('successfully uploaded')

@login_required
def renting(request): 
    if request.method == 'POST': 
        formA = ShareFormRent(request.POST, request.FILES)
        #formA = ShareFormA(request.POST, request.FILES)
        geolocator = Nominatim(user_agent= 'app' )

        if formA.is_valid():
            formA.instance.user = request.user
            #form.instance.created_by = request.user
            destination_ = formA.cleaned_data.get('zip_code')

            try:
                destination = geolocator.geocode(destination_)
                #print(destination)
                d_lat = int(destination.latitude)
                d_lon = int(destination.longitude)
                # formA.instance.lat = d_lat
                # formA.instance.lon = d_lon
                formA.instance.location = Point(d_lon, d_lat,srid=4326)
                formA.instance.Item_type = 'Rent'
                instance = formA.save(commit=False)
                instance.save() 
                messages.success(request, "Book shared successfully")
                return redirect('/')
            except:
                messages.error(request, "Inter a valid Zip Code")
                pass
    else: 
        formA = ShareFormRent()

    destination,l_lat, l_lon = get_destination(request)

    return render(request, 'productin-page.html', {'form' : formA, 'formtype' : 'Book Renting form', 'destination':destination,})

def SearchPage(request):
    srh = request.GET['query']
    products = Item.objects.filter(title__icontains=srh)
    item = Item.objects.all()[0:10]
    num_books = products.count()

    destination,l_lat, l_lon = get_destination(request)
    
    params = {'products': products, 'search':srh, 'items' : item, 'num_books':num_books ,'destination':destination }
    return render(request, 'search page.html', params)


def home(request):    

    destination,l_lat, l_lon = get_destination(request)
    user_location = Point( l_lon, l_lat, srid = 4326)
    queryset = Item.objects.annotate(distance=Distance('location',
    user_location, max_length=5)/1000
    ).order_by('distance')[0:20]

    #queryset_Motivation = Item.objects.filter(Item_type ='Rent')

    #print(Item.objects.values('Category'))
    # [{'Category': []}, {'Category': ['bb', 'dd', 'ff', 'gg']}, {'Category': ['dd', 'ff', 'gg']}, 
    # {'Category': ['cc', 'dd', 'ff']}, {'Category': ['aa', 'bb', 'dd', 'ff']}, {'Category': ['ee', 'gg']}, 
    # {'Category': ['dd', 'ff']}, {'Category': ['dd', 'gg']}, {'Category': ['gg']}]
    
    num_books = Item.objects.all().count()

    context = {
            #'items': Item.objects.all(),        
            'items': queryset,
            'num_books' : num_books,
            #'queryset_Motivation': queryset_Motivation,
            #'pointA' : pointA,
            'destination':destination,
        }

    return render(request, "home-page.html", context= context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            destination,l_lat, l_lon = get_destination(self.request)

            context = {
                'object' : order,
                'destination':destination,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You donot have active order")
            return redirect("app:home")

class OrderedSummaryView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=True)
            destination,l_lat, l_lon = get_destination(self.request)
            context = {
                'object' : order,
                'destination':destination,
            }
            return render(self.request, 'ordered_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You donot have any ordered item")
            return redirect("app:home")            

class ShareSummaryView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order=Share.objects.get(user=self.request.user, shared=False)
            destination,l_lat, l_lon = get_destination(self.request)
            context = {
                'object' : order,
                'destination':destination,
            }
            return render(self.request, 'share_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You donot have active share")
            return redirect("app:sharing")


# class ItemDetailView(DetailView):
#     model = Item
#     template_name = "product-page.html"
    

def ItemDetailView(request, slug):    
    item = get_object_or_404(Item, slug=slug)
    destination,l_lat, l_lon = get_destination(request)
    context = {
            'item':item,
            'destination':destination,
        }

    return render(request, "product-page.html", context= context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,user= request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug =item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"This item was updated")
            return redirect("app:order-summary")

        else:
            order.items.add(order_item)
            messages.info(request,"This was added to your cart")
            return redirect("app:order-summary" )

    else:
        ordered_date = timezone.now()
        order =Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This was added to your cart")
        return redirect("app:order-summary")
    
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                 ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug =item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This was removed to your cart")
            return redirect("app:order-summary")
        else:
            messages.info(request,"This was not in your cart")
            return redirect("app:product", slug=slug )

    else:
        messages.info(request,"you do not active order")
        return redirect("app:product", slug=slug )
    
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                 ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug =item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity  > 1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)
 
            messages.info(request,"This item quantity was updated")
            return redirect("app:order-summary")
        else:
            messages.info(request,"This was not in your cart")
            return redirect("app:product", slug=slug )

    else:
        messages.info(request,"you do not active order")
        return redirect("app:product", slug=slug )

@login_required
def increase_rent_time_interval(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
    order_item.rent_time_interval += 1
    order_item.save()
    messages.info(request,"This item was updated")
    return redirect("app:order-summary")

@login_required
def reduce_rent_time_interval(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
    if order_item.rent_time_interval  > 1:
        order_item.rent_time_interval-=1
        order_item.save()
    else:
        order_item.rent_time_interval = 1
        order_item.save()
    messages.info(request,"This item was updated")
    return redirect("app:order-summary")