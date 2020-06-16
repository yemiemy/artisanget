from django.urls import path
from .views import home, service, contact, privacy, terms, status, about, thank_you_page, feedback, signup_prompt

urlpatterns = [
	path('', home, name='home'),
    path('VIP-customer/signup-prompt/', signup_prompt, name='signup_prompt'),
    path('service/', service, name='service'),
    path('contact/', contact, name='contact'),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),
    path('status/', status, name='status'),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('thank-you/', thank_you_page, name='thank_you_page'),

]