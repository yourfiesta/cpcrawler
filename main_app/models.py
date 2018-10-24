from django.db import models
from django.utils import timezone
# Create your models here.

class ItemRank(models.Model):
    stt_de = models.CharField(max_length=8, blank=True, null=True)
    stt_tm = models.CharField(max_length=4, blank=True, null=True)
    site = models.CharField(max_length=50, blank=True, null=True)
    keyword = models.CharField(max_length=50, blank=True, null=True)
    rk = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=15)
    item_id = models.CharField(max_length=15)
    vendor_item_id = models.CharField(max_length=15)
  
    class Meta:
        managed = False
        db_table = u'item_rank'


class ItemSite(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    site = models.CharField(max_length=50, blank=True, null=True)
    keyword = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = u'item_site'

