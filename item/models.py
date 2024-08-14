from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH
from utils.constants import SITE_TYPE,START,END,UNIT_CHOICES,LOAD_CHOICES
from utils import utils_time
from parameter.models import Site,Goods,Vehicle,Project

# Create your models here.

class Item(models.Model):
    id = models.BigAutoField(primary_key=True)

    # all kinds of ids
    startsite_id = models.IntegerField(default=0)
    endsite_id = models.IntegerField(default=0)
    project_id = models.IntegerField(default=0)
    vehicle_id = models.IntegerField(default=0)
    goods_id = models.IntegerField(default=0)

    # parameter
    date = models.CharField(max_length=MAX_CHAR_LENGTH)
    unit = models.CharField(max_length=MAX_CHAR_LENGTH, choices=UNIT_CHOICES, default='time')
    quantity = models.FloatField(default=0)
    note = models.CharField(max_length=MAX_CHAR_LENGTH,null=True)
    load = models.CharField(max_length=MAX_CHAR_LENGTH, choices=LOAD_CHOICES, default='Own Equipment')

    # price
    contractorPrice = models.FloatField(default=0)
    startSubsidy = models.FloatField(default=0)
    endSubsidy = models.FloatField(default=0)
    endPayment = models.FloatField(default=0)
    driverPrice = models.FloatField(default=0)

    # info
    created_time = models.FloatField(default=utils_time.get_timestamp())
    if_delete = models.BooleanField(default=False)

    def get_load_display(self):
        return dict(LOAD_CHOICES).get(self.load, self.load)

    def serialize(self):
        start_site = Site.objects.filter(id=self.startsite_id).first()
        end_site = Site.objects.filter(id=self.endsite_id).first()
        goods = Goods.objects.filter(id=self.goods_id).first()
        project = Project.objects.filter(id=self.project_id).first()
        # Fetch all vehicles with IDs in vehicle_ids
        vehicle = Vehicle.objects.filter(id=self.vehicle_id).first()
        data = {
            "id":self.id,
            "start_site":start_site.serialize() if start_site else None,
            "end_site":end_site.serialize() if end_site else None,
            "vehicle":vehicle.serialize() if vehicle else None,
            "goods":goods.serialize() if goods else None,
            "project":project.serialize() if project else None,

            "note":self.note,
            "date":self.date,
            "unit":self.unit,
            "quantity":self.quantity,
            "load":self.load,

            "contractorPrice":self.contractorPrice,
            "startSubsidy":self.startSubsidy,
            "endSubsidy":self.endSubsidy,
            "endPayment":self.endPayment,
            "driverPrice":self.driverPrice,

            "created_time":self.created_time,
            "if_delete":self.if_delete
        }
        return data  