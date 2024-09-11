from .models import Subscription
import stripe
<<<<<<< HEAD
from django.shortcuts import redirect, reverse
from django.http import JsonResponse

def premium_required(function):
    def wrap(request, *args, **kwargs):
        # Check if user is premium
        if request.user.profile.is_premium:
            customer_stripe_id = Subscription.objects.filter(user_id=request.user).first()
            if customer_stripe_id:
                customer = stripe.Customer.retrieve(customer_stripe_id.customer_id)
                # Check subscription status
                active_subscription = any(sub.status in ['active', 'trialing', 'incomplete', 'past_due'] for sub in customer.subscriptions.data)
                if active_subscription:
                    return function(request, *args, **kwargs)

            # Mark profile as non-premium if subscription is not active
            request.user.profile.is_premium = False
            request.user.profile.save()
            return redirect(reverse('subscribe'))
        else:
            # Check if request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'redirect': reverse('subscribe')})
            return redirect(reverse('subscribe'))

    return wrap
=======
from django.shortcuts import render, redirect, reverse

def premium_required(function):
    def wrap(request, *args, **kwargs):
        
        if request.user.profile.is_premium:
            customer_stripe_id = Subscription.objects.filter(user_id=request.user).first()
            customer = stripe.Customer.retrieve(customer_stripe_id.customer_id)
            for sub in customer.subscriptions:
                    # If subscription is active or unpaid/cancelled but not yet inactive
                if sub.status == 'active' or sub.status == 'trialing' or sub.status == 'incomplete' or sub.status == 'past_due' or sub.status == 'canceled':
                    return function(request, *args, **kwargs)
            
            request.user.profile.is_premium = False
            return redirect(reverse('subscribe'))
        else:
            return redirect(reverse('subscribe'))
            
    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap
    

    
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
