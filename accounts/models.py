from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .paystack import PayStack
import secrets


Gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),  
)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    gender = models.CharField(max_length=200,null=False,choices=Gender, default='male')
    student_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Payment(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    verified=models.BooleanField(default=False)
    ref=models.CharField(max_length=200)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"Payment by :{self.email}"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref =ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100
            
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
            if self.verified:
                return True
            return False
