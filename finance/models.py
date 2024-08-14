from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH
from utils.constants import SITE_TYPE,START,END,UNIT_CHOICES
from utils import utils_time
from parameter.models import Site,Goods,Vehicle,Pay
# Create your models here.

class Advance(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    advance_time = models.CharField(max_length=MAX_CHAR_LENGTH)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    note = models.CharField(max_length=MAX_CHAR_LENGTH,default="无")
    pay_id = models.IntegerField(default=0)
    if_delete = models.BooleanField(default=False)

    def serialize(self):
        vehicle = Vehicle.objects.filter(id=self.vehicle_id).first()
        pay = Pay.objects.filter(id=self.pay_id).first()
        data = {
            "id":self.id,
            "vehicle":vehicle.serialize() if vehicle else None,
            "amount":self.amount,
            "advance_time":self.advance_time,
            "created_time":self.created_time,
            "note":self.note,
            "pay":pay.serialize() if pay else None,
            "if_delete":self.if_delete
        }
        return data  

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.CharField(max_length=MAX_CHAR_LENGTH)
    date = models.CharField(max_length=MAX_CHAR_LENGTH)
    amount = models.FloatField(default=0)
    pay_id = models.IntegerField(default=0)
    balance_amount = models.FloatField(default=0)
    note = models.CharField(max_length=MAX_CHAR_LENGTH)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    if_delete = models.BooleanField(default=False)

    def serialize(self):
        pay = Pay.objects.filter(id=self.pay_id).first()
        data = {
            "id":self.id,
            "owner":self.owner,
            "date":self.date,
            "amount":self.amount,
            "pay":pay.serialize() if pay else None,
            "balance_amount":self.balance_amount,
            "note":self.note,
            "created_time":self.created_time,
            "if_delete":self.if_delete
        }
        return data  