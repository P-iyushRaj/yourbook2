from django.contrib.gis.db import models
#from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator

PAYMENT_CHOICES = (
    ('S', 'Debit Card/Credit Card'),
    #('P', 'UPI'),
    ('COD', 'Cash on Delivery')
)

TYPE_CHOICES = (
    ('Se', 'Sell'),
    ('Rn', 'Rent')
    #('Bh', 'Both Rent & Sell')
)

CATEGORY_CHOICES = (
    ('aa', 'Science Fiction'),('bb','Romance'),('cc','Kids'),('dd','Youngster'),('ee','Old age'),
    ('ff', 'Student'), ('gg','Motivation'),

    ('ii', 'Class 6'), ('jj', 'Class 7'), ('kk', 'Class 8'), ('ll', 'Class 9'),
    ('mm', 'Class 11'),('nn', 'Class 12'), ('mm', 'NCERT')
)
    # ( 'Best Selling', (
    # ('aa', 'Science Fiction'),('bb','Romance'),('cc','Kids'),('dd','Youngster'),('ee','Old age'),
    # ('ff', 'Student'), ('gg','Motivation'),
    # )),

    # ('Student', (
    #         ('hh', 'School'),
    #         ('ii', 'College'),
    #     )),
    # )

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ACCOUNT_TYPE = (
    ( 'Sacc', 'Savings Account'),
    ( 'Oacc', 'Overdraft Account'),
    ( 'Cacc', 'Current Account')
)

import re
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# As model field:

def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)

def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
'''
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

#@receiver(post_save, sender=User)
    def create_or_update_user_profile(self, instance, created,*args, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
'''
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image

'''
class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')
'''

from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=100, default='', blank=True)

    description = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    address = models.CharField(max_length=100, default='', blank=True)
    #location = models.CharField(max_length=200, null=True, blank=True) #using ip of discovering man
    #distance = models.DecimalField(max_digits = 10, decimal_places=2, null=True, blank=True)

    website = models.URLField(default='', blank=True)
    phone = PhoneNumberField(blank=True)
    # phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
    # phone = models.CharField(validators=[phone_regex], max_length=17, blank = True, null= True)
    image = models.ImageField(upload_to='profile_images/', default='Shreyash.jpg',blank=True)
    #image = CloudinaryImage("sample").image(transformation={"crop": "fill","gravity": "faces","width": 300,"height": 200}, format="jpg")

    #london = UserProfileManager()
    Seller_Profile = models.ForeignKey(
        'SellerProfile', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        #img = Image.open(self.image.name)

        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/img/sample.jpg"


def create_profile(sender, **kwargs):
    if kwargs['created']:
        #user_profile = UserProfile.objects.create(user=kwargs['instance'])
        UserProfile.objects.create(user=kwargs['instance'])
'''       
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()
'''
post_save.connect(create_profile, sender=User)
'''
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''

from django.core.validators import RegexValidator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class PhoneOTP(models.Model):
    phone = PhoneNumberField(blank=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent', blank = True, null= True)
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful',
                        blank = True, null= True )

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


class SellerProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    companyName = models.CharField(max_length = 100, blank=True, null=True) #as in GST/PAN
    terms_condition = models.BooleanField(blank=True, null=True)
    phone = PhoneNumberField(blank=False)  #verify
    verified = models.BooleanField(default = False, help_text = 'If otp verification got successful',
                        blank = True, null= True )

    #Seller Information
    storeName = models.CharField(max_length = 100) #unique
    productCategory = models.CharField(blank=True, null=True,choices=CATEGORY_CHOICES, max_length=1)
                                        #will show to the user about your company product support
    zip = models.CharField(max_length=100)    # should show if the PINCODE has amazon sipping support
                                            # self shipping or company shippping
    address_1 = models.CharField(max_length = 100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = CountryField(multiple = False)

    #TAX details
    GST = models.CharField(max_length=50) # Yes / No
    #if yes
    tax_details = models.CharField(max_length=50)
    provisionalGSTIN = models.CharField(max_length= 100)
    PAN_number = models.CharField(max_length=100)

    #seller interview

    #Dashboard
         #start adding product -sharing/renting form

         #set shipping rates - self shipping or company shipping 
         #Enter Bank Details
    Account_holder_name = models.CharField(max_length=100)
    Account_type = models.CharField(blank=True, null=True,choices= ACCOUNT_TYPE, max_length=50)
    Account_number = models.CharField(max_length=100)
    ReEnter_account_number = models.CharField(max_length=100)
    IFSC_code = models.CharField(max_length=100)
         #Enter Tax details - PAN & GSTIN number
         #Product tax code  GST % differ for differ product
         #digital image signature
    signature = models.ImageField(upload_to='signature_images/', default='Shreyash.jpg',blank=True)



    def __str__(self):
        return self.user.username



from django.utils.translation import ugettext as _
from localflavor.in_.models import INStateField
class Item(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, blank = False)
    title = models.CharField(max_length=100)
    author= models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    #from localflavor.in_.models import INZipCodeField
    city = models.CharField(_("city"), max_length=64, default="Bengaluru")
    state = INStateField(_("state"), default="New Delhi")
    #zip_code = INZipCodeField(_("Zip"), default="812001")
    zip_code = models.CharField(_("zip code"), max_length=6, default="812001")

    # lon = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    # lat = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    Book_Img = models.ImageField(upload_to='images/')
    Book_Img2 = models.ImageField(upload_to='images/', null=True, blank=True)
    Book_Img3 = models.ImageField(upload_to='images/', null=True, blank=True)
    Book_Img4 = models.ImageField(upload_to='images/', null=True, blank=True)

    discount_price = models.FloatField(max_length=100, null=True, blank=True)
    rent_price = models.FloatField(max_length=100, blank=True, null = True)
    price = models.FloatField(max_length=100, null=True, blank=True)
    #rent= models.BooleanField(default=False)
    #sell= models.BooleanField(default=False)

    #Item_type = models.CharField(choices=TYPE_CHOICES, max_length=2, blank=True, null=True)
    Item_type = models.CharField(max_length=100, blank=True, null=True)
    #Category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, blank=True, null=True)
    Category = MultiSelectField(choices=CATEGORY_CHOICES,
                                 max_choices=20,
                                  max_length=20, blank=True, null=True)
    label = models.CharField(blank=True, null=True,choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.title} of {self.author}"

    def get_absolute_url(self):
        return reverse('app:product', kwargs= {'slug':self.slug } )

    def save(self, *args, **kwargs):
        slug_str = "%s %s %s" % (self.title, self.author, self.description)
        self.slug = slugify(slug_str)
        super().save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse('app:add-to-cart', kwargs= {'slug':self.slug })

    def get_remove_from_cart_url(self):
        if not self.slug:
            slug_str = "%s %s %s" % (self.title, self.author, self.description)
            self.slug = slugify(slug_str)
            return reverse("app:remove-from-cart", kwargs={'slug':self.slug})

# class rent(models.Model):
#     rent_price = models.FloatField(max_length=100, blank=True, null = True)

# class sell(models.Model0):


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
   
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    rent_time_interval = models.IntegerField(
        default=1
        # validators=[
        #     MaxValueValidator(12),
        #     MinValueValidator(1)
        # ]
     )

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def total_rent_price(self):
        return self.quantity * self.item.rent_price * self.rent_time_interval

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        elif self.item.rent_price:
            return self.total_rent_price()
        return self.get_total_item_price()

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    #ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True
    )
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length = 100)
    apartment_address = models.CharField(max_length=100)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    #phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    phone = PhoneNumberField(blank=False)
    country = CountryField(multiple = False)
    zip = models.CharField(max_length=100) 
    payment_option = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #payment_option = models.CharField(max_length=50)
    #item = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True, blank=True)
    #payment_option = item.payment_option
    
    
    def __str__(self):
        #print(self.item.payment_option)
        return f"{self.user.username} pay {self.amount}"

class ShareItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    shared = models.BooleanField(default=False)
   
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def total_rent_price(self):
        return self.item.rent_price() * self.item.rent_time_interval()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        elif self.item.rent_price(self):
            return self.total_rent_price()
        return self.get_total_item_price()
    
class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    #ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(ShareItem)
    start_date = models.DateTimeField(auto_now_add=True)
    shared_date = models.DateTimeField()
    shared = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

