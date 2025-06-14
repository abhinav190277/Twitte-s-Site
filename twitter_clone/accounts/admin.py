from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birth_date']
    list_filter = ['location', 'birth_date']
    search_fields = ['user__username', 'user__email']