<<<<<<< HEAD
from .models import ChatMessage,FileUpload
=======
from .models import Messages, Conversations
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
from django import forms
from django.forms import Textarea

class MessageForm(forms.ModelForm):

    class Meta:
<<<<<<< HEAD
        model = ChatMessage
        fields = ('message_content', )


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
=======
        model = Messages
        fields = ('message_content', )

>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
# class SmallMessageForm(forms.ModelForm):

#     class Meta:
#         model = Messages
#         fields = ('message_content', )        
#         widgets = {
<<<<<<< HEAD
#           'message_content': Textarea(attrs={'rows':3, 'cols':50}),}
=======
#           'message_content': Textarea(attrs={'rows':3, 'cols':50}),}
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
