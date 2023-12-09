from django.contrib import admin

# Register your models here.
from .models import *

class ContactAdmin(admin.ModelAdmin):
  list_display = ('email', 'phone', 'contact_date')
  list_display_links = ('phone', 'email')
  search_fields = ('email', 'phone')
  list_per_page = 25


class PaymentAdmin(admin.ModelAdmin):
  list_display = ('email', 'first_name', 'last_name', 'created_at')
  list_display_links = ('first_name', 'email')
  search_fields = ('email', 'first_name')
  list_per_page = 25

class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'level',)
  list_display_links = ('user', 'level')
  search_fields = ('level', 'user')
  list_per_page = 25

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Profile,ProfileAdmin)
