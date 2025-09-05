from django.db import models
from users.models import User
from business.models import Business

# Create your models here.
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('open','Open'),
            ('closed','Closed'),
            ('escalated','Escalated')
        ],
        default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"ChatSession {self.user} & {self.business}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_details')
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('business', 'Business'),
            ('agent','Agent'),
            ('admin', 'Admin')
        ],
        default='user'
    )
    message = models.TextField()
    payload = models.JSONField(null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.sender} - {self.session}"
    