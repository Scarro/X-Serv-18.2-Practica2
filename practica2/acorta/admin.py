from django.contrib import admin
from .models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ('url_completa', 'url_scheme', 'url_acortada')

admin.site.register(Url, UrlAdmin)