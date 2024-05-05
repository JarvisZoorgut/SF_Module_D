from django.contrib import admin
from .models import Advertisement, Response
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Advertisement)
admin.site.register(Response)

# Apply summernote to all TextField in model.
class AdvertisementAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'