from django.contrib import admin
from .models import Banner  # Import the Banner model


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    search_fields = ['title']