from django.contrib import admin
from .models import Contact, Privacy, Term, Service, Order, Feedback
# Register your models here.
admin.site.register(Contact)
admin.site.register(Privacy)
admin.site.register(Term)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Feedback)