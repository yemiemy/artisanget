from django.shortcuts import render, redirect
from .models import Contact, Privacy, Term, Service, Order, Feedback
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django import forms 
from django.views.generic.base import TemplateView
from win10toast import ToastNotifier
from plyer import notification
# Create your views here.

def home(request):
    services = Service.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        description = request.POST['description']
        service = request.POST['service']
        service = Service.objects.get(id=service)
        city = request.POST['city']
        state = request.POST['state']
        accept_term = request.POST['accept']

        register = Order.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            service=service,
            description=description,
            accept_term=accept_term,
            date_stamp=datetime.now()
            )
        register.save()
        notification.notify(title="ArtisanGet", message="Your Order has been successfully placed! We will contact you soon.")
        messages.success(request, 'Your Order has been successfully placed! We will contact you soon.')
        context = {
          'name':name,
          'email':email,
          'mobile':mobile,
          'address': address,
          'city':city,
          'state':state,
          'service':service,
          'description':description,
          'accept_term':accept_term
        }
        subject = 'Service Order Form'
        body = render_to_string('register.txt', context)
        send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])

        ##send notification to customer
        contexts = {
            'user': name,
            'order_id': service
        }
        message= render_to_string('notification_message.txt', contexts)
        head = f'Your ArtisanGet Order {service} has been successfully confirmed!'
        send_mail(head, message, 'rasholayemi@gmail.com', [email])

        return redirect('signup_prompt')

    return render(request, 'index.html', {
        'year':datetime.now().year,
        'services':services,
        'title':'Home',
        })

def signup_prompt(request):
    return render(request, 'signup_prompt.html', {})

def service(request):
    return render(request, 'services.html', {'year':datetime.now().year, 'title':'Service',})


def status(request):
    if request.method == 'POST':
        email = request.POST['email']
        mobile = request.POST['mobile']
        try:
            user = Order.objects.filter(email=email)
        except:
            user = None

        if user:
            notification.notify(title="ArtisanGet", message="Your Order is being processed! We will contact you soon.")
            messages.success(request, 'Your order is being processed. We will contact you soon.')
            context = {
              'email':email,
              'mobile':mobile,
            }
            subject = 'Service Order Look Up Form'
            body = render_to_string('order.txt', context)
            send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])
        else:
            messages.warning(request, 'Are you sure you are registered? We can not find this user.')
        

    return render(request, 'status.html', {
        'year':datetime.now().year,
        'title':'Track Order',
        })

def privacy(request):
    privacy = Privacy.objects.all().order_by('-id')
    return render(request, 'privacy.html', {'year':datetime.now().year,'privacy':privacy, 'title':'Privacy',})

def terms(request):
    terms = Term.objects.all().order_by('-id')
    return render(request, 'terms.html', {'year':datetime.now().year,'terms':terms, 'title':'Terms',})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']


        contact = Contact.objects.create(name=name, email=email, message=message, date_stamp = datetime.now())
        contact.save()
        notification.notify(title="ArtisanGet", message="Your message has been successfully sent! We will contact you shortly.")
        messages.success(request, 'Your message has been successfully sent! We will contact you soon.')
        
        context = {
          'email':email,
          'name':name,
          'message':message,
        }
        subject = 'Campus Service contact form'
        body = render_to_string('contact.txt', context)
        send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])
    return render(request, 'contact.html', {'year':datetime.now().year, 'title':'Contact',})

def about(request):
    feedback = Feedback.objects.all().order_by('-id')
    return render(request, 'about.html', {'year':datetime.now().year, 'feedback':feedback, 'title':'About Us',})

def thank_you_page(request):
    return render(request, 'thank.html', {'year':datetime.now().year, 'title':'Thank You',})


def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        rate = request.POST['rate']
        price = request.POST['price']
        efficiency = request.POST['efficiency']


        feedback = Feedback.objects.create(name=name, email=email, rate=rate,price=price, efficiency=efficiency, date_stamp = datetime.now())
        feedback.save()
        notification.notify(title="ArtisanGet", message="Your Feedback has been successfully received! Thanks for choosing us.")

        context = {
          'email':email,
          'name':name,
          'rate':rate,
          'price':price,
          'efficiency':efficiency,
        }
        subject = 'Campus Service Feedback form'
        body = render_to_string('feedback.txt', context)
        send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])
        return redirect('thank_you_page')
    return render(request, 'feedback.html', {'year':datetime.now().year, 'title':'FeedBack',})