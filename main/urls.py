from main import views
from django.urls import path
urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about ,name="about"),
    path('schedule/', views.schedule, name="schedule"),
    path('register/', views.register, name="register"),
    path('contact/', views.contact, name="contact"),
    path('handle-contact/', views.handle_contact, name="handle_contact"),
    path('sponsorship/', views.sponsorship, name="sponsorship"),
    path('subscribe/', views.subscribe_to_brevo, name='subscribe_to_brevo'),
    
    # Flutterwave sponsorship payment endpoints
    path('api/sponsorship-tiers/', views.get_sponsorship_tiers_json, name='get_sponsorship_tiers'),
    path('api/initiate-sponsorship-payment/', views.initiate_sponsorship_payment, name='initiate_sponsorship_payment'),
    path('api/verify-sponsorship-payment/', views.verify_sponsorship_payment, name='verify_sponsorship_payment'),
    path('api/sponsorship-status/', views.get_sponsorship_status, name='get_sponsorship_status'),
    path('api/webhooks/flutterwave/', views.flutterwave_webhook, name='flutterwave_webhook'),
]
