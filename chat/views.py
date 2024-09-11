<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import MessageForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage, Winks, Views, Block, Call, FileUpload
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from checkout.decorators import premium_required
from django.db import models
import json
from django.views.decorators.http import require_POST

@login_required
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)

    if user_to_block == request.user:
        return JsonResponse({'error': 'You cannot block yourself.'}, status=400)

    if Block.objects.filter(blocker=request.user, blocked=user_to_block).exists():
        return JsonResponse({'message': 'User already blocked.'}, status=400)

    Block.objects.create(blocker=request.user, blocked=user_to_block)
    return JsonResponse({'message': 'User blocked successfully.'})

@login_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)

    block = Block.objects.filter(blocker=request.user, blocked=user_to_unblock).first()
    if not block:
        return JsonResponse({'error': 'User is not blocked.'}, status=400)

    block.delete()
    return JsonResponse({'message': 'User unblocked successfully.'})

@login_required
def new_message_check(request):
    conversation_id = request.GET.get('url_id', None)
    if not conversation_id:
        return JsonResponse({'error': 'No conversation ID provided'}, status=400)

    conversation = get_object_or_404(ChatSession, id=conversation_id)
    is_read = ChatMessage.objects.filter(chat_session=conversation, receiver=request.user, is_read=False).exists()

    return JsonResponse({'conversation': is_read})

@login_required
def read_messages(request):
    conversation_id = request.GET.get('url_id', None)
    if not conversation_id:
        return JsonResponse({'error': 'No conversation ID provided'}, status=400)

    conversation = get_object_or_404(ChatSession, id=conversation_id)
    messages = ChatMessage.objects.filter(chat_session=conversation, receiver=request.user, is_read=False)

    messages.update(is_read=True)

    is_read = not ChatMessage.objects.filter(chat_session=conversation, receiver=request.user, is_read=False).exists()

    return JsonResponse({'conversation': is_read})

@login_required
def chat(request, id):
    page_ref = "chat"
    conversation_ids = ChatSession.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:
        all_conversations[conversation.id] = ChatMessage.objects.filter(chat_session=conversation).last()

        last_message = ChatMessage.objects.filter(chat_session=conversation, receiver=request.user).last()
        if last_message:
            is_read_check[conversation.id] = last_message.is_read
        else:
            is_read_check[conversation.id] = True

    sorted_conversations = sorted(all_conversations.items(), key=lambda x: x[1].created_on, reverse=True)

    ChatMessage.objects.filter(chat_session=id, receiver=request.user, is_read=False).update(is_read=True)

    messages = ChatMessage.objects.filter(chat_session=id)
    conversation = ChatSession.objects.get(pk=id)
    participants = conversation.participants.all()

    receiver = None
    for user in participants:
        if user.id != request.user.id:
            receiver = user
            break

    if request.method == "POST":
        if 'send_message' in request.POST:
            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                if receiver.id == request.user.id:
                    messages.error(request, "You can't send a message to yourself")
                    return redirect(reverse('chat_home'))

                message = message_form.save(commit=False)
                message.receiver = receiver
                message.sender = request.user
                message.chat_session = conversation
                message.save()

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{receiver.id}',
                    {
                        'type': 'chat_message',
                        'message': message.message_content,
                        'sender': request.user.username
                    }
                )

                send_mail(
                    subject='New Message Notification',
                    message=f'You have received a new message from {request.user.username}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver.email],
                    fail_silently=False,
                )

                return redirect(reverse('chat', kwargs={'id': id}))

        elif 'start_voice_call' in request.POST:
            return redirect(reverse('start_call', kwargs={'receiver_id': receiver.id, 'call_type': 'voice'}))

        elif 'start_video_call' in request.POST:
            return redirect(reverse('start_call', kwargs={'receiver_id': receiver.id, 'call_type': 'video'}))

        elif 'block_user' in request.POST:
            response = block_user(request, receiver.id)
            return JsonResponse(response)

    else:
        message_form = MessageForm()

    context = {
        'page_ref': page_ref,
        'user_messages': messages,
        'message_form': message_form,
        'all_conversations': sorted_conversations,
        'receiver': receiver.id if receiver else None,
        'conversation_id': int(id),
        'is_read_check': is_read_check
    }

    return render(request, 'chat.html', context)

# Chat home page, which displays all conversations but no messages



@login_required
def chat_home(request):
    conversations = ChatSession.objects.filter(participants=request.user).annotate(
        latest_message_time=models.Max('messages__created_on')
    ).order_by('-latest_message_time')

    all_conversations = {}
    is_read_check = {}

    for conversation in conversations:
        # Fetch messages that haven't been marked as deleted by the current user
        last_message = ChatMessage.objects.filter(
            chat_session=conversation
        ).exclude(deleted_for=request.user).order_by('-created_on').first()

        if not last_message:
            continue  # Skip if no visible messages for this user

        all_conversations[conversation.id] = last_message

        # Check if there are unread messages that haven't been deleted
        unread_message = ChatMessage.objects.filter(
            chat_session=conversation,
            sender=request.user,
            is_read=False
        ).exclude(deleted_for=request.user).exists()

        is_read_check[conversation.id] = not unread_message

    unopened_messages = ChatMessage.objects.filter(
        sender=request.user,
        is_read=False
    ).exclude(deleted_for=request.user).count()

    context = {
        'all_conversations': all_conversations,
        'is_read_check': is_read_check,
        'unopened_messages': unopened_messages,
    }

    return render(request, 'chat_home.html', context)



#
# @csrf_exempt
# @login_required


@require_POST
@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(ChatSession, id=conversation_id)

    # Ensure the logged-in user is a participant in the conversation
    if request.user in conversation.participants.all():
        # Fetch all messages in this conversation that haven't already been deleted for this user
        messages_to_delete = ChatMessage.objects.filter(
            chat_session=conversation
        ).exclude(deleted_for=request.user)

        # Mark each message as deleted for this user
        for msg in messages_to_delete:
            msg.deleted_for.add(request.user)
            msg.save()

        # If all participants have deleted this conversation, delete it from the database
        all_deleted = all([request.user in msg.deleted_for.all() for msg in conversation.messages.all()])
        if all_deleted:
            conversation.delete()
        else:
            conversation.save()

        messages.info(request, 'Conversation deleted successfully')
        return redirect('chat_home')

    return HttpResponseBadRequest("Invalid request")




# AJAX function to create wink record
def wink(request):
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        data = {}
        data['message'] = "You can't wink at yourself, cheeky!"
        return JsonResponse(data)

    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id) & Q(is_read=False)).exists()
    if current_wink:
        data = {}
        data['message'] = "Member hasn't viewed your last wink yet"
        return JsonResponse(data)

    wink = Winks(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    data = {}
    try:
        wink.save()

        # Send email notification to the receiver
        send_mail(
            subject='New Wink Notification',
            message=f'You have received a new wink from {request.user.username}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[wink.receiver.email],
            fail_silently=False,
        )

        data['message'] = 'Wink successfully sent.'
    except:
        data['message'] = 'Something went wrong. Wink not sent'

    return JsonResponse(data)

"""
AJAX function to create reject record. Used for quick match feature so as not to
display a rejected user again
"""
def reject(request):
    # Get id of reject recipient
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        return HttpResponse(status=204)

    # Check if a reject record for these users already exists, if so do nothing
    current_reject = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id)).exists()
    if current_reject:
        return HttpResponse(status=204)

    # Create reject record
    reject = Reject(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    data = {}
    try:
        reject.save()
    except:
        data['message'] = 'Something went wrong. Profile not skipped.'
    finally:
        data['message'] = 'Member successfully skipped'
    return JsonResponse(data)

# AJAX function to create a messages/conversation record(s)
@login_required
def chat_ajax(request):
    receiver_id = request.POST.get('message_receiver')
    message_content = request.POST.get('message_content')

    if receiver_id == str(request.user.id):
        return JsonResponse({"message": "You can't send a message to yourself"})

    # Get the receiver user
    try:
        receiver = User.objects.get(pk=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({'message': "Receiver does not exist"})

    # Check if a conversation exists between the sender and receiver
    conversation = ChatSession.chat_session_exists(request.user, receiver)

    if conversation and request.user in conversation.user_deletion.all():
        # If the conversation is deleted by the user, create a new conversation
        conversation = None

    if not conversation:
        # Create a new conversation if none exists or if the old one was deleted
        conversation = ChatSession.create_if_not_exists(request.user, receiver)

    # Create a new message
    message = ChatMessage(
        chat_session=conversation,
        receiver=receiver,
        sender=request.user,
        message_content=message_content,
        is_read=False
    )
    message.save()

    # Update the last message time
    conversation.last_message_time = message.created_on
    conversation.save(update_fields=['last_message_time'])

    data = {'message': "Message sent successfully"}

    # Send email notification to the receiver
    try:
        send_mail(
            subject='New Message Notification',
            message=f'You have received a new message from {request.user.username}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({'message': f"Message sent but email failed: {str(e)}"})

    return JsonResponse(data)



# Winks page to display recieved winks
@login_required
@premium_required
def winks(request):

    # Query recieved winks and paginate results
    # Assistance from https://docs.djangoproject.com/en/1.11/topics/pagination/
=======
from django.shortcuts import render, reverse, redirect, render_to_response
from .forms import MessageForm
from .models import Conversations, Messages, Winks, Views
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from profiles.views import looking_for_check
import time
from checkout.decorators import premium_required
from django.contrib.auth.decorators import login_required
# error message checks needed

@login_required
@premium_required
def new_message_check(request):
    conversation_id = request.GET.get('url_id', None)
    is_read = Messages.objects.filter(conversation=conversation_id, receiver=request.user, is_read=False).exists()
    data = {
        'conversation': is_read
    }
    return JsonResponse(data)
    
def read_messages(request):
    conversation_id = request.GET.get('url_id', None)
    messages = Messages.objects.filter(conversation=conversation_id)
    for message in messages:
        if message.receiver == request.user:
            message.is_read = True
            message.save()
            
    is_read = Messages.objects.filter(conversation=conversation_id, receiver=request.user, is_read=False).exists()
    data = {
        'conversation': is_read
    }
    return JsonResponse(data)

@login_required
@premium_required
def chat(request, id):
    
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()

        # Make one db query
        if Messages.objects.filter(conversation=conversation, receiver=request.user).last():
            last_received_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last() 
            is_read_check[conversation.id] = last_received_message.is_read
        else: 
            is_read_check[conversation.id] = True
    
    messages = Messages.objects.filter(conversation=id)
        
    conversation = Conversations.objects.get(pk=id)
    participants = conversation.participants.all()
    for user in participants:
        if not user.id == request.user.id:
            receiver = user
        
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            if receiver.id == request.user.id:
                messages.success(request, "You can't send a message to yourself")
                return redirect(reverse('chat_home'))
            
            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=receiver.id)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            
        context = {
            'user_messages': messages,
            'message_form':message_form,
            'all_conversations': all_conversations,
            'receiver': receiver,
            'conversation_id': int(id),
            'is_read_check': is_read_check
        }
        return HttpResponseRedirect("/chat/%s" % id)
    else:
        message_form = MessageForm()
    
    context = {
        'user_messages': messages,
        'message_form':message_form,
        'all_conversations': all_conversations,
        'receiver': receiver.id,
        'conversation_id': int(id),
        'is_read_check': is_read_check
    }
    
    return render(request, 'chat.html', context)
  
@login_required  
@premium_required 
def chat_home(request):
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:  
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()

        # Make one db query
        if Messages.objects.filter(conversation=conversation, receiver=request.user).last():
            last_received_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last() 
            is_read_check[conversation.id] = last_received_message.is_read
        else: 
            is_read_check[conversation.id] = True

    context = {
        'user_messages': messages,
        'all_conversations': all_conversations,
        'conversation_id': None,
        'is_read_check': is_read_check
    }

    return render(request, 'chat_home.html', context)
    
# Get rid of?
def create(request):
    
    # message_form = MessageForm()
    
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            conversation = Conversations()
            conversation.save()
            conversation.participants.add(request.user, 39)

            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=2)
            message.sender = request.user
            message.save()
    else:
        message_form = MessageForm()
        
    context = {
        'message_form': message_form
    }
    
    return render(request, 'create.html', {'message_form':message_form})

def wink(request):
    # Change None backup?
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        messages.success(request, "You can't send a wink to yourself, cheeky")
        return redirect(reverse('index'))
    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id) & Q(is_read=False)).exists()
    if current_wink:
        # messages.success(request, "Your last wink hasn't been seen yet. Try again later.")
        print("not seen")
        return HttpResponse(status=204)
    
    wink = Winks(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    try:
        wink.save()
    except:
        # messages.success(request, "Something went wrong. Wink not sent")
        print("not sent")
    finally:
        # messages.success(request, "Wink successfully sent.")
        print("sent")
    # pass messages using https://stackoverflow.com/questions/52483675/how-to-filter-django-annotations-on-reverse-foreign-key-fields
    return HttpResponse(status=204)

@login_required
@premium_required
def chat_ajax(request):
    receiver_id = request.POST.get('message_receiver')
    message_content = request.POST.get('message_content')
    
    if receiver_id == request.user.id:
        messages.success(request, "You can't send a message to yourself")
        return redirect(reverse('index'))
    
    conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=receiver_id)
    if conversation.exists():
        try:
            message = Messages(
            receiver=User.objects.get(pk=receiver_id),
            sender=request.user,
            message_content=message_content,
            is_read=False,
            conversation=conversation[0]
            )
            message.save()
        except:
            # Errors
            print("Error report")
    else:
        try:
            conversation = Conversations()
            conversation.save()
            conversation.participants.add(request.user.id)
            conversation.participants.add(User.objects.get(pk=receiver_id))
            message = Messages(
                receiver=User.objects.get(pk=receiver_id),
                sender=request.user,
                message_content=message_content,
                is_read=False,
                conversation=conversation
                )
            message.save()
        except:
            # Errors
            print("Error report")
            
    return HttpResponse(status=204)
    
@login_required
def winks(request):
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)

    page = request.GET.get('page')
<<<<<<< HEAD
=======
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    try:
        winks_page = winks_paginated.page(page)
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
        page = 1
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)
        page = winks_paginated.num_pages
<<<<<<< HEAD


    context = {
        'page_ref': 'wink',
        'winks_page': winks_page,
        'page': page
    }


    return render(request, 'winks.html', context)

# Views page to display recieved views
@login_required
@premium_required
def views(request):

    # Query recieved winks and paginate results
=======
        
    
    context = {
        'winks_page': winks_page,
        'page': page
    }
    
    
    return render(request, 'winks.html', context)

@login_required
@premium_required   
def views(request):

>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)

    page = request.GET.get('page')
<<<<<<< HEAD
=======
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    try:
        views_page = views_paginated.page(page)
    except PageNotAnInteger:
        views_page = views_paginated.page(1)
        page = 1
    except EmptyPage:
        views_page = views_paginated.page(views_paginated.num_pages)
        page = views_paginated.num_pages
<<<<<<< HEAD

    context = {
        'page_ref': 'view',
        'views_page': views_page,
        'page': page
    }

    return render(request, 'views.html', context)

# AJAX function to read all winks currently on specific page
@login_required
def read_wink(request):

    page = request.GET.get('page', None)

    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)

=======
        
    context = {
        'views_page': views_page,
        'page': page
    }
    
    return render(request, 'views.html', context)

@login_required
def read_wink(request):
    
    page = request.GET.get('page', None)
    
    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
    winks_paginated = Paginator(winks, 6)
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    try:
        winks_page = winks_paginated.page(page)
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)
<<<<<<< HEAD

    for wink in winks_page:
        wink.is_read = True
        wink.save()

    return HttpResponse(status=204)

# AJAX function to read all views currently on specific page
@login_required
@premium_required
def read_view(request):
    page = request.GET.get('page', None)

    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)

=======
    
    for wink in winks_page:
        wink.is_read = True
        wink.save()
        
    return HttpResponse(status=204)

@login_required
@premium_required
def read_view(request):
    
    page = request.GET.get('page', None)
    
    views = Views.objects.filter(receiver=request.user.id).order_by('-created_on')
    views_paginated = Paginator(views, 6)
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    try:
        views_page = views_paginated.page(page)
    except PageNotAnInteger:
        views_page = views_paginated.page(1)
    except EmptyPage:
        views_page = views_paginated.page(views_paginated.num_pages)
<<<<<<< HEAD

    for view in views_page:
        view.is_read = True
        view.save()

    return HttpResponse(status=204)
=======
    
    for view in views_page:
        view.is_read = True
        view.save()
        
    return HttpResponse(status=204)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
