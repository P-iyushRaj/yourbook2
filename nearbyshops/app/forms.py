from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *

from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext as _

PAYMENT_CHOICES = (
    ('S', 'Debit Card/Credit Card'),
    #('P', 'UPI'),
    ('COD', 'Cash on Delivery')
)


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'name','phone', 'address')


'''
class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = UserProfile
        fields = (
            'image',
            'name',
            'address',
            'phone',
            
        )
'''


class SellerRegisterForm(forms.Form):
    companyName = forms.CharField(required=True, widget=forms.TextInput(attrs={
        #'placeholder' : 'pustkalaya'
    }))
    terms_condition = forms.BooleanField(required=True)

class mobileverification(forms.Form):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('7407993331')}), 
                label=_("Phone number"), required=True)

class ValidatePhoneSendOTPform(forms.Form):
    otp = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder' : 'enter OTP'
    }))

# class sendOTPform(forms.Form):
#     class Meta:
#         model = PhoneOTP
#         fields = ['phone']

# class recieveOTPform(forms.Form):
#     class Meta:
#         model = PhoneOTP
#         fields = ['otp']        
#PhoneNumberField

class ShareForm(forms.ModelForm):
    class Meta:
        model = Item

        fields = ['title', 'author', 'description','Category', 'city','state','zip_code',
            'Book_Img',
            'Book_Img2', 'Book_Img3', 'Book_Img4', 'price','discount_price',
            ]

class ShareFormRent(forms.ModelForm):
    class Meta:
        model = Item

        fields = ['title', 'author', 'description', 'Category', 'city','state','zip_code',
        'Book_Img',
        'Book_Img2', 'Book_Img3', 'Book_Img4', 'rent_price',
        ]
'''
class ShareFormA(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'Book Name'
    }))
    author = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'Book Author'
    }))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'Your feedback about the book and its condition'
    }))

    price = forms.FloatField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'price printed on book'
    }))

    discount_price = forms.FloatField(required=False, widget=forms.FloatField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'discounted price'
    })))

    category = forms.ChoiceField(required=False,
        widget=forms.RadioSelect, choices=CATEGORY_CHOICES)


    destination= models.CharField(max_length=200, null=True, blank=True) # from the sharing form
    lon = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    lat = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(max_digits = 10, decimal_places=2, null=True, blank=True)

    Book_Img = models.ImageField(upload_to='images/')
    Book_Img2 = models.ImageField(upload_to='images/', null=True, blank=True)
    Book_Img3 = models.ImageField(upload_to='images/', null=True, blank=True)
    Book_Img4 = models.ImageField(upload_to='images/', null=True, blank=True)

    
    #rent= models.BooleanField(default=False)
    #sell= models.BooleanField(default=False)
    rent_price = models.FloatField(blank=True, null = True)
        
    rent_time_interval = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
     )

    
    payment = models.CharField(blank=True, null=True, choices=PAYMENT_CHOICES, max_length=3)
    label = models.CharField(blank=True, null=True,choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(max_length=300, blank=True, null=True)

    description = models.TextField()


    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : '1234 Main St'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control'
    }))

'''
#if sell if rent price


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : '1234 Main St'
    }))

    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : 'Apartment or suite'
    }))

    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('7407993331')}), 
                    label=_("Phone number"), required=True)

    #shipping_address = forms.CharField(required=False)
    #shipping_address2 = forms.CharField()
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))

    # City = CityField(blank_label='(select country)').formfield(
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control'
    }))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    #set_default_shipping = forms.BooleanField(required=False)
    #use_default_shipping = forms.BooleanField(required=False)
    '''
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    billing_addre ss = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    '''


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
