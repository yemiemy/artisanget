from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from phone_field import PhoneField
# Create your models here.

class OrderLookUp(models.Model):
    email = models.EmailField(max_length=250)
    mobile = models.CharField(max_length=11)


class Service(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=250)
    mobile = PhoneField(help_text='Contact phone number')
    address = models.TextField()
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    accept_term = models.BooleanField(default=False) 
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} placed an order on {self.date_stamp}' 


class Privacy(models.Model):
    body = RichTextUploadingField()
    date_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural ='Privacies'

class Term(models.Model):
    body = RichTextUploadingField()
    date_stamp = models.DateTimeField(auto_now_add=True)
class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=250)
    message = models.TextField(null=True, blank=True)
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} messaged on {self.date_stamp}' 

class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=250)
    rate = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    efficiency = models.TextField(null=True, blank=True)
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} messaged on {self.date_stamp}' 