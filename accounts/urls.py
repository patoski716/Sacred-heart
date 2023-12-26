from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('staff/', views.staff, name='staff'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('account_settings/', views.edit, name="account_settings"),
    path('fees/', views.initiate_payment, name="fees"),
    path('success/<str:ref>/', views.verify_payment, name='verify-payment'),
    path('history/', views.history, name='history'),
    path('detail/<pk>/', views.detail, name="detail"),
    path('profile/', views.profile, name="profile")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)