from django.db import models

# Create your models here.
class Recipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Mail(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    cta_text = models.CharField(max_length=100, blank=True, null=True)
    cta = models.URLField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject