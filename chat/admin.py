from django.contrib import admin
<<<<<<< HEAD
from .models import ChatMessage, ChatSession, Winks, Reject
#
# # Register your models here.
#
class MessageAdmin(admin.ModelAdmin):
    model = ChatMessage
    list_display = ('sender', 'receiver', 'message_content', 'created_on', 'is_read')
#
class ConversationAdmin(admin.ModelAdmin):
    model = ChatSession
    list_display = ('id', )
#
class WinkAdmin(admin.ModelAdmin):
    model = Winks
    list_display = ('sender', 'receiver',  'created_on', 'is_read')
#
class RejectAdmin(admin.ModelAdmin):
    model = Reject
    list_display = ('sender', 'receiver',  'created_on')
#
admin.site.register(ChatMessage, MessageAdmin)
admin.site.register(Winks, WinkAdmin)
admin.site.register(ChatSession, ConversationAdmin)
admin.site.register(Reject, RejectAdmin)
=======
from .models import Messages, Conversations, Winks

# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    model = Messages
    list_display = ('sender', 'receiver', 'message_content', 'created_on', 'is_read')
    
class ConversationsAdmin(admin.ModelAdmin):
    model = Conversations
    list_display = ('id', )
    
class WinksAdmin(admin.ModelAdmin):
    model = Winks
    list_display = ('sender', 'receiver',  'created_on', 'is_read')

admin.site.register(Messages, MessagesAdmin)
admin.site.register(Winks, WinksAdmin)
admin.site.register(Conversations, ConversationsAdmin)
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
