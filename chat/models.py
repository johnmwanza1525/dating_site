from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.db.models import Q
import uuid
class ChatSession(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    last_message_time = models.DateTimeField(auto_now=True,null=True)
    user_deletion = models.ManyToManyField(User, related_name="deleted_conversations", blank=True)

    def __str__(self):
        return '_'.join(participant.username for participant in self.participants.all())

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    @staticmethod
    def chat_session_exists(user1, user2):
        return ChatSession.objects.filter(participants=user1).filter(participants=user2).first()

    @staticmethod
    def create_if_not_exists(user1, user2):
        chat_sessions = ChatSession.objects.filter(participants=user1)
        for session in chat_sessions:
            if session.participants.filter(id=user2.id).exists():
                return session
        # If no session exists, create a new one
        chat_session = ChatSession.objects.create()
        chat_session.participants.add(user1, user2)
        return chat_session


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages",null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages",null=True)
    message_content = models.TextField(max_length=500,null=True)
    message_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('file', 'File')], default='text')
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    is_read = models.BooleanField(default=False)
    is_typing = models.BooleanField(default=False)  # Indicator if the user is typing
    # Keep track of users who deleted this message
    deleted_for = models.ManyToManyField(User, related_name='deleted_messages', blank=True)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.created_on} - {self.sender.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.chat_session.last_message_time = self.created_on
        self.chat_session.save(update_fields=['last_message_time'])

    @staticmethod
    def count_overall_unread_msg(user_id):
        total_unread_msg = 0
        user_all_sessions = ChatSession.objects.filter(participants__id=user_id)
        for session in user_all_sessions:
            unread_msg_count = ChatMessage.objects.filter(chat_session=session, is_read=False).exclude(sender__id=user_id).count()
            total_unread_msg += unread_msg_count
        return total_unread_msg

    @staticmethod
    def mark_message_as_read(message_id):
        msg_inst = ChatMessage.objects.get(id=message_id)
        msg_inst.is_read = True
        msg_inst.save(update_fields=['is_read'])

    @staticmethod
    def mark_all_messages_as_read(room_id, user):
        all_msgs = ChatMessage.objects.filter(chat_session_id=room_id, is_read=False).exclude(sender=user)
        for msg in all_msgs:
            msg.is_read = True
            msg.save(update_fields=['is_read'])


class Winks(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_winks",null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_winks",null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    is_read = models.BooleanField(default=False)


class Views(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_views",null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_views",null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    is_read = models.BooleanField(default=False)


class Reject(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_rejects",null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_rejects",null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)


class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_users",null=True)
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocking_users",null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)


class Call(models.Model):
    CALL_TYPES = [
        ('voice', 'Voice'),
        ('video', 'Video'),
    ]

    CALL_STATUS = [
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('ringing', 'Ringing'),
        ('answered', 'Answered'),
        ('declined', 'Declined'),
    ]

    caller = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="outgoing_calls")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="incoming_calls")
    call_type = models.CharField(max_length=10, choices=CALL_TYPES)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=CALL_STATUS, default='initiated')
    signaling_data = models.JSONField(null=True, blank=True)
    is_muted = models.BooleanField(default=False)
    is_screen_sharing = models.BooleanField(default=False)


class FileUpload(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True,null=True)
=======
    
class Conversations(models.Model):
    participants = models.ManyToManyField(User, related_name="participants", unique=False)

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", unique=False)
    conversation = models.ForeignKey(Conversations, related_name="conversations")
    message_content = models.TextField(max_length=500, default='', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)
    
class Winks(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)

class Views(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)  
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
