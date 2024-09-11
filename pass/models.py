from django.db import models
from django.contrib.auth.models import User
#from PIL import Image
from django.utils import timezone
import uuid

# Create your models here.
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username}"
