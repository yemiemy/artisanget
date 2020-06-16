from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm, ProfileArtisanUpdateForm
from django.contrib import messages
from .models import Order, Service, Skill, Message
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .utils import id_generator
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, ListView
from django.contrib.auth.models import User
from win10toast import ToastNotifier
from django.views.generic.base import TemplateView
from plyer import notification

##chat
from django.utils.safestring import mark_safe
import json
# Create your views here.

class ServiceWorker(TemplateView):
    template_name = "mobile/sw.js"
    content_type = "application/javascript"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


@login_required
def profile(request):
    orders = Order.objects.all().order_by('-id')[:5]
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(
                request, 'Your profile has been updated!'
                )
            notification.notify(
                title="ArtisanGet", 
                message="Your profile has been successfully updated!"
                )
            
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'user.html', {'p_form':p_form, 'u_form':u_form, 'orders':orders})

@login_required
def artisan_signup(request):
    skills = Skill.objects.all()
    if request.method == 'POST':
        a_form = ProfileArtisanUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if a_form.is_valid():
            a_form.save()
            messages.success(request, 'Your application as an artisan has been received! You will receive a mail soon.')
            
            notification.notify(title="ArtisanGet", message="Your application as an artisan has been received! You will receive a mail soon.")

            context = {
            'name':request.user,
            'email':request.user.email,
            'skill':request.user.profile.skill
            }
            subject = 'Application As a Service Provider'
            body = render_to_string('artisan.txt', context)
            send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])

            contexts = {
            'user': request.user.first_name,
            'skill':request.user.profile.skill
            }
            message= render_to_string('arstisan_message.txt', contexts)
            head = f'Your application as ArtisanGet artisan has been received!'
            send_mail(head, message, 'rasholayemi@gmail.com', [request.user.email])
            
            return redirect('dashboard')
    else:
        a_form = ProfileArtisanUpdateForm(instance=request.user.profile)
    return render(request, 'artisan_signup.html', {'a_form':a_form, 'skills':skills})

@login_required
def dashboard(request):
    user = request.user

    ######## Customer Section
    orders = Order.objects.filter(user=request.user).order_by('-id')
    objs = Order.objects.filter(user=request.user).order_by('-id')[:1]
    for obj in objs:
        if obj.accepted:
            #remove order from processing
            obj.processing = False
            obj.save()
            # Notify user of a new message
            chats = Message.objects.filter(author=obj.accepted_by)[0]
            if chats:
                messages.success(
                    request, 'Check your inbox, you have a new message. You can send a message to your artisan.'
                    )
                notification.notify(
                    title="ArtisanGet", 
                    message=f'You have a new message. You can send a message to your artisan.'
                    )
            
            # Get the price from the customer
            if request.method == 'POST':
                price = request.POST['price']
                obj.price_by_customer = price
                obj.save()
                messages.success(
                    request, 
                    f'Your response has been recorderd for Order {obj.order_id} successfully!'
                    )
                notification.notify(
                    title="ArtisanGet", 
                    message=f'Your response has been recorderd for Order {obj.order_id} successfully!'
                    )
            
            # send mail to user if the order is accepted and not complerted.
            if obj.completed == False:
                messages.success(
                    request, 
                    f'Your ArtisanGet Order {obj.order_id} has been successfully Accepted by {obj.accepted_by.first_name}!'
                    )
                notification.notify(
                    title="ArtisanGet", 
                    message=f'Your ArtisanGet Order {obj.order_id} has been successfully Accepted by {obj.accepted_by.first_name}!'
                    )

                # contexts = {
                # 'user': request.user.first_name,
                # 'service':obj.service.name,
                # 'accepted_by':obj.accepted_by.first_name,
                # 'order_id': obj.order_id
                # }
                # message = render_to_string('accepted_message.txt', contexts)
                # head = f'Your ArtisanGet Order {obj.order_id} has been successfully Accepted by {obj.accepted_by.first_name}!'
                # send_mail(head, message, 'rasholayemi@gmail.com', [request.user.email])
        
        #Send a mail to user if order is completed.
        # if obj.completed:
        #     if obj.price_by_artisan == obj.price_by_customer:
        #         print('passed customer')
        #         messages.success(request, f'Your order {obj.order_id} has been completed! Thanks for patronage.')
        #         contexts = {
        #         'user': request.user.first_name,
        #         'service':obj.service.name,
        #         'order_id': obj.order_id
        #         }
        #         message = render_to_string('completed_message.txt', contexts)
        #         head = f'Your ArtisanGet Order {obj.order_id} has been successfully completed!'
        #         send_mail(head, message, 'rasholayemi@gmail.com', [request.user.email])

    # counters
    com_count = 0
    for order in orders:
        if order.completed == True:
            com_count = com_count + 1

    ord_count = 0
    for order in orders:
        ord_count = ord_count + 1
    pro_count = 0
    for order in orders:
        if order.processing == True:
            pro_count = pro_count + 1
    #### End of  Customer Section ######

######## Artisan section #############
    accepted_orders = Order.objects.all().order_by('-id')
    objects = Order.objects.all().order_by('-id')[:1]
    #Electrician  
    acc_count = 0
    for order in accepted_orders:
        if order.service.name == 'Electrical Services':
            if order.accepted_by == request.user:
                acc_count = acc_count + 1
    completed_count = 0
    for order in accepted_orders:
        if order.service.name == 'Electrical Services':
            if order.completed_by == request.user:
                completed_count = completed_count + 1

    #Plumbers
    plum_count = 0
    for order in accepted_orders:
        if order.service.name == 'Plumbing Services':
            if order.accepted_by == request.user:
                plum_count = plum_count + 1
    completed_plum = 0
    for order in accepted_orders:
        if order.service.name == 'Plumbing Services':
            if order.completed_by == request.user:
                completed_plum = completed_plum + 1

    #Carpenters
    car_count = 0
    for order in accepted_orders:
        if order.service.name == 'Carpentry Services':
            if order.accepted_by == request.user:
                car_count = car_count + 1
    car_com = 0
    for order in accepted_orders:
        if order.service.name == 'Carpentry Services':
            if order.completed_by == request.user:
                car_com = car_com + 1

    #Furniture
    fur_count = 0
    for order in accepted_orders:
        if order.service.name == 'Furniture making':
            if order.accepted_by == request.user:
                fur_count = fur_count + 1
    fur_com = 0
    for order in accepted_orders:
        if order.service.name == 'Furniture making':
            if order.completed_by == request.user:
                fur_com = fur_com + 1

    #Cleaner
    clean_count = 0
    for order in accepted_orders:
        if order.service.name == 'Cleaning Services':
            if order.accepted_by == request.user:
                clean_count = clean_count + 1
    clean_com = 0
    for order in accepted_orders:
        if order.service.name == 'Cleaning Services':
            if order.completed_by == request.user:
                clean_com = clean_com + 1

    #Painter
    paint_count = 0
    for order in accepted_orders:
        if order.service.name == 'Painting Services':
            if order.accepted_by == request.user:
                paint_count = paint_count + 1
    paint_com = 0
    for order in accepted_orders:
        if order.service.name == 'Painting Services':
            if order.completed_by == request.user:
                paint_com = paint_com + 1
    #### End of Section ######
    return render(request, 'dashboard.html', {
        'orders':orders, 
        'user':user,
        'ord_count':ord_count,
        'pro_count':pro_count,
        'com_count':com_count,
        'objects':objects,
        'completed_count':completed_count,
        'completed_plum':completed_plum,
        'acc_count':acc_count,
        'car_count':car_count,
        'car_com':car_com,
        'plum_count':plum_count,
        'clean_count':clean_count,
        'clean_com':clean_com,
        'paint_count':paint_count,
        'paint_com':paint_com,
        'fur_count':fur_count,
        'fur_com':fur_com,
        'accepted_orders':accepted_orders,
        'date':datetime.now()
        })

class UserNotificationsView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'notifications.html'
    context_object_name = 'orders'
    #paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Order.objects.filter(user=user).order_by('-id')[:5]




@login_required
def order(request):
    try:
        orders = Order.objects.all().order_by('-id')[:5]
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
                user=request.user,
                name=name,
                email=email,
                mobile=mobile,
                address=address,
                description=description,
                city=city,
                state=state,
                service=service,
                accept_term=accept_term,
                order_id=id_generator(),
                date_stamp=datetime.now()
                )
            register.save()
            id_order = register.order_id

            notification.notify(title="ArtisanGet", message= f"Hello {name}, your Order has been successfully placed! We will contact you soon. ORDER ID: {id_order}")

            messages.success(request, f'Your order has been successfully placed! We will contact you soon. ORDER ID: {id_order}')
            context = {
            'name':name,
            'email':email,
            'mobile':mobile,
            'address': address,
            'description':description,
            'city':city,
            'state':state,
            'service':service,
            'accept_term':accept_term
            }
            subject = 'Service Order Form'
            body = render_to_string('register.txt', context)
            send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])

            contexts = {
                'user': request.user.first_name,
                'order_id': id_order
            }
            message= render_to_string('notification_message.txt', contexts)
            head = f'Your ArtisanGet Order {id_order} has been successfully confirmed!'
            send_mail(head, message, 'rasholayemi@gmail.com', [email])
            return redirect('dashboard')
    except Exception as e:
        return render(request, 'error/exception.html', {'e':e})
    return render(request, 'order.html', {'services':services, 'orders':orders})

def order_accept(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        order.accepted = True
        order.accepted_by = request.user
        order.save()

        if request.method == 'POST':
            price = request.POST['price']
            order.price_by_artisan = price
            order.completed = True
            order.completed_by = request.user
            order.save()
            print(order.price_by_customer)
            print(order.price_by_artisan)
            if order.price_by_customer == order.price_by_artisan:
                print('passed artisan')
                messages.success(request, f'You have successfully completed Order {order.order_id}')

                contexts = {
                    'user': request.user.first_name,
                    'order_id':order.order_id
                }
                message= render_to_string('arstisan_complete.txt', contexts)
                head = f'You have successfully completed Order {order.order_id}'
                send_mail(head, message, 'rasholayemi@gmail.com', [request.user.email])
            return redirect('dashboard')
    except Exception as e:
        return render(request, 'error/exception.html', {'e':e})
    return render(request, 'order_accept.html', {'object':order})

@login_required
def status(request):
    try:
        orders = Order.objects.all().order_by('-id')[:5]
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            order_id = request.POST['order_id']
            try:
                order = Order.objects.get(order_id=order_id)
            except:
                order = None

            if order:
                notification.notify(title="ArtisanGet", message=f"Hello {name}, Your order with ID {order_id} is being processed! We will contact you soon.")
                messages.success(request, f'Your order with ID {order_id} is being processed. We will contact you soon.')
                context = {
                    'name':name,
                    'email':email,
                    'mobile':mobile,
                    'order_id':order_id
                }
                subject = 'Service Order Look Up Form'
                body = render_to_string('users/order.txt', context)
                send_mail(subject, body, 'rasholayemi@gmail.com', ['contact@artisanget.com'])
            else:
                messages.warning(request, f'Are you sure you placed an order? We can not find this order with ID {order_id}. HINT: make sure the Order ID is in upper case')
    except Exception as e:
        return render(request, 'error/exception.html', {'e':e})
    return render(request, 'track-status.html', {'orders':orders})


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = '/dashboard/user-dashboard'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False


@login_required
def room(request, username):
    return render(request, 'chat.html', {
        'room_name_json': mark_safe(json.dumps(username)),
        'username': mark_safe(json.dumps(request.user.username)),
    })