from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Paygroup(models.Model):
    group_name = models.CharField(max_length=500, default='')




class Receipt(models.Model):
    name = models.CharField(max_length= 300, default = '')
    date = models.DateField(auto_now_add=True)
    info = models.TextField(default='')
    dic = models.TextField(default='')
    completed = models.BooleanField(default=False)
    notcompletedlist = models.CharField(max_length = 1000, default='')
    completedlist = models.CharField(max_length=1000, default='')
    totlist= models.CharField(max_length=1000, default='')
    venmo_id = models.CharField(max_length = 200, default='')
    src = models.TextField(default='')
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    venmo_name = models.CharField(max_length=500, blank=True)
    group = models.ManyToManyField(Paygroup)
    receipts = models.ManyToManyField(Receipt)
    accumulated = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)


# For linking the profiles to the django user class when calling save()
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


