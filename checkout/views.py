<<<<<<< HEAD
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import OrderForm
from .models import Subscription, Order
from profiles.models import Profile
from .utils import initiate_mpesa_payment, verify_mpesa_payment
import logging

logger = logging.getLogger(__name__)

def make_user_premium(user):
    profile = Profile.objects.get(user=user)
    profile.is_premium = True
    profile.save()
=======
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm, MakePaymentForm
from .models import Subscription
from django.utils import timezone
import stripe
from profiles.models import Profile

# Check redirect reverse are working
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

def make_user_premium(request):
    profile = Profile.objects.get(user_id=request.user.id)
    profile.is_premium = True
    profile.save()
    
    return
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)

@login_required
def subscribe(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
<<<<<<< HEAD
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.user = request.user

            # Validate phone number format
            if not order.phone_number.startswith('254'):
                messages.error(request, "Please enter a valid M-Pesa phone number starting with '254'.")
                return redirect('subscribe')

            order.save()

            # Initiate M-Pesa payment
            redirect_url = request.build_absolute_uri(reverse('mpesa_callback', args=[order.id]))
            try:
                payment_response = initiate_mpesa_payment(
                    amount=order.get_plan_price(),
                    phone_number=order.phone_number,
                    reference=str(order.id),
                    description=f"Subscription for {order.get_plans_display()}"
                )

                # Debug: log the payment response
                logger.info(f"M-Pesa payment response: {payment_response}")

                if payment_response and payment_response.get('ResponseCode') == '0':
                    messages.success(request, "M-Pesa payment initiated. Complete the payment on your phone.")
                    return redirect(reverse('mpesa_callback', args=[order.id]))
                else:
                    logger.error(f"M-Pesa payment initiation failed: {payment_response}")
                    messages.error(request, f"Error initiating M-Pesa payment: {payment_response.get('ResponseDescription', 'Unknown error')}. Please try again.")
                    return redirect(reverse('subscribe'))
            except Exception as e:
                logger.exception("Exception during M-Pesa payment initiation:")
                messages.error(request, f"Error initiating M-Pesa payment: {str(e)}. Please try again.")
                return redirect(reverse('subscribe'))
    else:
        order_form = OrderForm()

    return render(request, 'subscribe.html', {'page_ref': 'subscribe', 'order_form': order_form})

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Order
from profiles.models import Profile

@login_required
def mpesa_callback(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        payment_status = verify_mpesa_payment(order.id)

        if payment_status == 'Completed':
            subscription = Subscription.objects.create(
                user=request.user,
                plan=order.plans,
                mpesa_code=order_id  # Assuming order_id is the unique identifier
            )
            make_user_premium(request.user)

            # Send successful subscription email
            send_mail(
                'Subscription Successful',
                f'Hello {request.user.username},\n\nYour payment has been successful. You have been subscribed to the {order.get_plans_display()} plan.\n\nYour subscription starts today and will expire on {subscription.expiry_date}.',
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )

            # Notify user 2 days before expiry
            notify_expiry(subscription)

            messages.success(request, "Payment successful! You are now a premium user.")
            return render(request, 'success.html')
        else:
            messages.error(request, "Payment verification failed or was not completed. Please try again.")
            return render(request, 'fail.html')
    except Order.DoesNotExist:
        messages.error(request, "Order does not exist.")
        return redirect(reverse('subscribe'))

    return redirect(reverse('index'))


def notify_expiry(subscription):
    # Calculate when to send expiry notification
    reminder_date = subscription.expiry_date - timedelta(days=2)
    if reminder_date < timezone.now().date():
        send_mail(
            'Subscription Expiry Notice',
            f'Hello {subscription.user.username},\n\nYour subscription for the {subscription.plan} plan will expire soon on {subscription.expiry_date}.\n\nPlease renew your subscription to continue enjoying premium features.',
            'from@example.com',
            [subscription.user.email],
            fail_silently=False,
        )
=======
        payment_form = MakePaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            print(order.plans)
            
            customer = stripe.Customer.list(email=request.user.email)
            # customer = Subscription.objects.filter(user_id=request.user.id).first()
            # If customer already exists
            if customer:
                """
                Stripe returns a list of customers, as there shouldn't be any more
                one customer from a email query, the first of the list is used. If
                more than one is returned, the latest active account would be used.
                """
                active_customer = customer.data[0]
                # Merge into one try
                try:
                    print("updating customer")
                    stripe.Customer.modify(
                        active_customer.id,
                        card = payment_form.cleaned_data['stripe_id']
                    )
                # Add error messages
                except:
                    print('error')
                    return redirect(reverse('checkout'))
                    
                try:
                    print("updating sub")
                    stripe.Subscription.create(
                        customer = active_customer.id,
                        items=[{"plan": order.plans,},]
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('checkout'))
                finally:
                    subscription = Subscription(
                            user = request.user, 
                            plan = "Monthly", 
                            customer_id = active_customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
            else:
            # If new customer
                try:
                    customer = stripe.Customer.create(
                        email = request.user.email,
                        plan = order.plans,
                        description = request.user.email,
                        card = payment_form.cleaned_data['stripe_id'],
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect(reverse('checkout'))
                
                finally:
                # Add check if subscription created successfully (will need to change paid
                # https://stripe.com/docs/api/customers/create)
                # if customer.paid:
                #     messages.error(request, "You have paid successfully")
                #     return redirect(reverse('index'))
                    subscription = Subscription(
                            user = request.user, 
                            # Make custom
                            plan = "Monthly", 
                            customer_id = customer.id
                            )
                    subscription.save()
                    make_user_premium(request)
                
                # else:
                #     messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "Unable to take payment")
            print(order_form.errors)
            print(payment_form.errors)
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
      
    return render(request, 'subscribe.html', {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})

>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
