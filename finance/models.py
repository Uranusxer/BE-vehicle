from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH
from utils.constants import SITE_TYPE,START,END,UNIT_CHOICES
from utils import utils_time
from parameter.models import Site,Goods,Vehicle
# Create your models here.

class Advance(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    advance_time = models.CharField(max_length=MAX_CHAR_LENGTH)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    if_delete = models.BooleanField(default=False)

    def serialize(self):
        vehicle = Vehicle.objects.filter(id=self.vehicle_id).first()
        data = {
            "id":self.id,
            "vehicle":vehicle.serialize() if vehicle else None,
            "amount":self.amount,
            "advance_time":self.advance_time,
            "created_time":self.created_time,
            "if_delete":self.if_delete
        }
        return data  