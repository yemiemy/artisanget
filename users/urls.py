from django.urls import path
from .views import (
    profile, dashboard, status, order, OrderDeleteView, UserNotificationsView, 
    ServiceWorker, 
    artisan_signup, order_accept, room)


urlpatterns = [
    path('user-profile/', profile, name='profile'),
    path('user-dashboard/', dashboard, name='dashboard'),
    #path('notifications/', notifications, name='notification'),
    path('track-status/', status, name='track-status'),
    path('place-order/', order, name='place-order'),
    path('dashboard/order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('user/orders/<str:username>/', UserNotificationsView.as_view(), name='user-orders'),
    path('make-money/0/a/artisan-signup/', artisan_signup, name='artisan_signup'),
    path('accept-order/<int:id>/', order_accept, name='order_accept'),
    #path('order/chat/<int:id>/<str:username>/', chat, name='chat'),
    
    path('chat/<str:username>/', room, name='chat'),
    #path('<str:username>/user-dashboard/', UserDashboardListView.as_view(), name='dashboard'),

    
    path('', ServiceWorker.as_view(), name="service-worker"),
]