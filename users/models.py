from django.db import models
from django.contrib.auth import get_user_model
from phone_field import PhoneField

from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Create your models here.

User = get_user_model()

class Skill(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    about_me = models.TextField(blank=True, null=True)
    phone = PhoneField(help_text='Contact phone number')
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, blank=True, null=True)
    is_customer = models.BooleanField(blank=True, null=True, default=True)
    proficiency = models.IntegerField(blank=True, null=True)
    experience = models.CharField(max_length=120,blank=True, null=True)
    efficiency = models.IntegerField(blank=True, null=True)
    time_conscious = models.BooleanField(blank=True, null=True)
    standout = models.CharField(max_length=250, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    electrician = models.BooleanField(default=False)
    plumber = models.BooleanField(default=False)
    furniture = models.BooleanField(default=False)
    painter = models.BooleanField(default=False)
    cleaner = models.BooleanField(default=False)
    carpenter = models.BooleanField(default=False)
    facebook = models.CharField(max_length=150, blank=True, null=True)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

class Service(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=250)
    mobile = models.CharField(max_length=11)
    address = models.TextField()
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price_by_customer = models.IntegerField(blank=True, null=True)
    price_by_artisan = models.IntegerField(blank=True, null=True)
    accept_term = models.BooleanField(default=False) 
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    processing = models.BooleanField(default=True)
    abandoned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='completed')
    accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='artisan')
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} placed order on {self.date_stamp}' 



class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username 
    def last_10_messages():
        return Message.objects.all()[:0]
