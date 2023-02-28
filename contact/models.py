from django.db import models
from django.core.validators import EmailValidator
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, validators=[EmailValidator,])
    subject = models.CharField(max_length=100, blank=False)
    message = models.TextField()
    contacted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
    
    def __str__(self):
        return str(self.email)