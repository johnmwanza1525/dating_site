from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from datetime import timedelta

class Order(models.Model):
    PLANS = (
        ('plan_F5eyGdYCvZPtON', '1 Month'),
        ('plan_F5ey2nnZwy5v8Q', '2 Months'),
        ('plan_F5eyNlWXHig7YB', '3 Months'),
    )

    PLAN_PRICES = {
        'plan_F5eyGdYCvZPtON': 1,
        'plan_F5ey2nnZwy5v8Q': 650,
        'plan_F5eyNlWXHig7YB': 1000,
    }

    plans = models.CharField(choices=PLANS, max_length=100, blank=False)
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)  # New field for storing safaricom stk payload

    def get_plan_price(self):
        return self.PLAN_PRICES.get(self.plans, 0)

    def __str__(self):
        return f"{self.id} - {self.date} - {self.full_name}"

class Subscription(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    plan = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    mpesa_code = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True,null=True)
    expiry_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            # Calculate expiry date based on plan duration
            plan_durations = {
                'plan_F5eyGdYCvZPtON': 30,
                'plan_F5ey2nnZwy5v8Q': 60,
                'plan_F5eyNlWXHig7YB': 90,
            }
            duration = plan_durations.get(self.plan, 30)
            self.expiry_date = self.start_date + timedelta(days=duration)
        super().save(*args, **kwargs)
=======

# Create your models here.

class Order(models.Model):
    PLANS = (
        ('plan_F5eyGdYCvZPtON', 'Monthly - £24.99'),
        ('plan_F5ey2nnZwy5v8Q', '3 Months - £49.99'),
        ('plan_F5eyNlWXHig7YB', '6 Months - £74.99'),
        )
    plans = models.CharField(choices=PLANS, default='plan_F5ey2nnZwy5v8Q', blank=False, max_length=100)
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField()
    
    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)

# Change to subscriptionlineitem with user attribute
class Subscription(models.Model):
    user = models.ForeignKey(User, null=False)
    plan = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
