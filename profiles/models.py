from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from chat.models import ChatSession
from checkout.models import Subscription
from django.db.models.signals import post_save, pre_delete
=======
from django.db.models.signals import post_save
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
import os
import math
from django.db.models.expressions import RawSQL
<<<<<<< HEAD
import stripe
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import os


"""
Only necessary for local and testing sqlite databases
As SQLite does not support math functions, the following function adds the
capability for it to do so
"""
if "DEVELOPMENT" in os.environ or "TESTING" in os.environ:
    @receiver(connection_created)
    def extend_sqlite(connection=None, **kwargs):
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)

class LocationManager(models.Manager):
    
    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, citylat, citylong, max_distance=None):
=======
import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    # sqlite doesn't natively support math functions, so add them
    cf = connection.connection.create_function
    cf('acos', 1, math.acos)
    cf('cos', 1, math.cos)
    cf('radians', 1, math.radians)
    cf('sin', 1, math.sin)

class LocationManager(models.Manager):
    # def nearby_locations(self, cityLat, cityLong, radius=100, use_miles=True):
    #     # if use_miles:
    #     #     distance_unit = 3959
    #     # else:
    #     distance_unit = 6371
        
    #     from django.db import connection, transaction
    #     from django.conf import settings
    #     cursor = connection.cursor()
    #     # As certain math functions not usable in sqlite, this check is used to make them available
    #     # Uses Haversine formula to determine radius to check for close values
    #     # Assistance from https://stackoverflow.com/questions/1916953/filter-zipcodes-by-proximity-in-django-with-the-spherical-law-of-cosines
    #     if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    #         connection.connection.create_function('acos', 1, math.acos)
    #         connection.connection.create_function('cos', 1, math.cos)
    #         connection.connection.create_function('radians', 1, math.radians)
    #         connection.connection.create_function('sin', 1, math.sin)
        
    #     sql = """SELECT id, (acos(sin(radians(%f)) * sin(radians(cityLat)) + cos(radians(%f))
    #       * cos(radians(cityLat)) * cos(radians(%f-cityLong))) * %d)
    #     AS distance FROM profiles_profile WHERE distance < %f
    #     ORDER BY distance;""" % (cityLat, cityLat, cityLong, distance_unit, radius)
    #     cursor.execute(sql)
    #     ids = [row[0] for row in cursor.fetchall()]
        
    #     return self.filter(id__in=ids)
    
    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, cityLat, cityLong, max_distance=None):
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        gcd_formula = "6371 * acos(cos(radians(%s)) * \
<<<<<<< HEAD
        cos(radians(citylat)) \
        * cos(radians(citylong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(citylat)))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (citylat, citylong, citylat)
        )
    
=======
        cos(radians(cityLat)) \
        * cos(radians(cityLong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(cityLat)))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (cityLat, cityLong, cityLat)
        )
    
        # qs = Profile.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
        # Better way for this?
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        if max_distance is not None:
            return self.annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
        else:
            return self.annotate(distance=distance_raw_sql)

<<<<<<< HEAD
class custom_admin(models.Model):
    """Passing Custom Admin Attributes"""
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(unique=True)
    pic= models.ImageField(upload_to='admin_pic',blank=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name = 'profile_detail')
    email = models.EmailField(unique=True,null=True)
=======

# def get_locations_nearby_coords(self, cityLat, cityLong, max_distance=None):
#         """
#         Return objects sorted by distance to specified coordinates
#         which distance is less than max_distance given in kilometers
#         """
        
        
#         gcd_formula = "6371 * acos(cos(radians(%s)) * \
#         cos(radians(cityLat)) \
#         * cos(radians(cityLong) - radians(%s)) + \
#         sin(radians(%s)) * sin(radians(cityLat)))"
#         distance_raw_sql = RawSQL(
#             gcd_formula,
#             (cityLat, cityLong, cityLat)
#         )
#         qs = Profile.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
#         if max_distance is not None:
#             qs = qs.filter(distance__lt=max_distance)
#         return qs

class Profile(models.Model):
    # Limit username 11 chars
    user = models.OneToOneField(User, on_delete=models.CASCADE)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    bio = models.TextField(max_length=500, default='', blank=False)
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A LITTLE EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
        ('BOTH', 'Both'),
    )
<<<<<<< HEAD

=======
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved')
    )
    ETHNICITY = (
        ('WHITE', 'White'),
        ('ASIAN: INDIAN', 'Asian: Indian'),
        ('ASIAN: PAKISTANI', 'Asian: Pakistani'),
        ('ASIAN: BANGLADESHI', 'Asian: Bangladeshi'),
        ('ASIAN: CHINESE', 'Asian: Chinese'),
        ('BLACK', 'Black'),
        ('MIXED', 'Mixed'),
        ('OTHER ETHNICITY', 'Other Ethnicity')
    )
    RELATIONSHIP_STATUS = (
        ('NEVER MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated')
    )
    EDUCATION = (
    ('HIGH SCHOOL', 'High School'),
    ('COLLEGE', 'College'),
    ('BACHELORS DEGREE', 'Bachelors Degree'),
    ('MASTERS', 'Masters'),
    ('PHD / POST DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"))
<<<<<<< HEAD

    gender = models.CharField(choices=GENDER, default="MALE", max_length=6)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    ethnicity = models.CharField(choices=ETHNICITY, default="BLACK", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER MARRIED", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
=======
    
    gender = models.CharField(choices=GENDER, default="MALE", max_length=6)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER MARRIED", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=100, decimal_places=2)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10)
    body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='', blank=False)
<<<<<<< HEAD
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True,null=True)
    objects = LocationManager()
    is_online = models.BooleanField(default = False)
    
    # Assistance from https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

# Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
=======
    cityLat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    cityLong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)
    
    objects = LocationManager()
    
    # https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

# https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)
    
<<<<<<< HEAD
from django.utils.html import mark_safe

class ProfileImage(models.Model):
    PIC_APPROVAL = (
=======
class ProfileImage(models.Model):
    
    APPROVAL = (
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
<<<<<<< HEAD

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_filename, blank=True)
    is_verified = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True,null=True)

    def thumbnail(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe(f'<img src="{self.image.url}" width="150" />')
        return 'No Image Available'

    thumbnail.short_description = 'Thumbnail'  # Display name in the admin interface

=======
    
    user = models.ForeignKey(User, default=None)
    image = models.ImageField(upload_to=image_filename, blank=True)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
<<<<<<< HEAD

post_save.connect(create_user_profile, sender=User)

def pre_delete_user(sender, instance, **kwargs):
    # Before user deleted, delete all conversations they were participants of
    conversations = ChatSession.objects.filter(participants=instance.id)
    for conversation in conversations:
        conversation.delete()
    
    # Before user deleted, cancel all subscriptions
    customer = Subscription.objects.filter(user_id=instance.id).first()
    try:
        if customer:
            stripe_customer = stripe.Customer.retrieve(customer.customer_id)
            for sub in stripe_customer.subscriptions.data:
                stripe.Subscription.modify(
                    sub.id,
                    cancel_at_period_end=True
                )
    except:
        print('Pre-delete user failed')
        
pre_delete.connect(pre_delete_user, sender=User)
=======
    
post_save.connect(create_user_profile, sender=User)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
