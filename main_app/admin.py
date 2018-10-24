from django.contrib import admin

# Register your models here.

from  .models import ItemRank
from .models import ItemSite

class ItemSiteAdmin(admin.ModelAdmin):
        list_display = ('user_id', 'site', 'keyword')

admin.site.register(ItemSite)
admin.site.register(ItemRank)

