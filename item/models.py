from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH
from utils.constants import SITE_TYPE,START,END,UNIT_CHOICES
from utils import utils_time
from parameter.models import Site,Goods,Vehicle
# Create your models here.

class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    startsite_id = models.IntegerField(default=0)
    endsite_id = models.IntegerField(default=0)
    vehicle_id = models.IntegerField(default=0)
    goods_id = models.IntegerField(default=0)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    start_date = models.CharField(max_length=MAX_CHAR_LENGTH)
    end_date = models.CharField(max_length=MAX_CHAR_LENGTH)
    unit = models.CharField(max_length=MAX_CHAR_LENGTH, choices=UNIT_CHOICES, default='time')
    contractorPrice = models.FloatField(default=0.0)
    startSubsidy = models.FloatField(default=0.0)
    endSubsidy = models.FloatField(default=0.0)
    endPayment = models.FloatField(default=0.0)
    driverPrice = models.FloatField(default=0.0)
    if_delete = models.BooleanField(default=False)

    def serialize(self):
        start_site = Site.objects.filter(id=self.startsite_id).save()
        end_site = Site.objects.filter(id=self.endsite_id).save()
        vehicle = Vehicle.objects.filter(id=self.vehicle_id).save()
        goods = Goods.objects.filter(id=self.goods_id).save()
        data = {
            "id":self.id,
            "startsite":start_site.serialize() if start_site else None,
            "end_site":end_site.serialize() if end_site else None,
            "vehicle":vehicle.serialize() if vehicle else None,
            "goods":goods.serialize() if goods else None,
            "start_date":self.start_date,
            "end_date":self.end_date,
            "unit":self.unit,
            "contractorPrice":self.contractorPrice,
            "startSubsidy":self.startSubsidy,
            "endSubsidy":self.endSubsidy,
            "endPayment":self.endPayment,
            "driverPrice":self.driverPrice,
            "created_time":self.created_time,
            "if_delete":self.if_delete
        }
        return data  