from django.contrib import admin
from .models import Profile, Service, Order, Skill, Message
# Register your models here.
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Skill)
admin.site.register(Message)