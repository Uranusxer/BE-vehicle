from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH
from utils.constants import SITE_TYPE,START,END
from utils import utils_time
# Create your models here.

class Site(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH,unique=True)
    manager = models.CharField(max_length=MAX_CHAR_LENGTH,null=True)
    manager_phone = models.BigIntegerField(default=0,null=True)
    type = models.CharField(max_length=20,choices=SITE_TYPE,default=START)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    def serialize(self):
        data = {
            "id":self.id,
            "name":self.name,
            "manager":self.manager,
            "manager_phone":self.manager_phone,
            "created_time":self.created_time
        }
        return data     

class Goods(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    created_time = models.FloatField(default=utils_time.get_timestamp())
    def serialize(self):
        data = {
            "id":self.id,
            "name":self.name,
            "created_time":self.created_time
        }
        return data
    
class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    driver = models.CharField(max_length=MAX_CHAR_LENGTH)
    license = models.CharField(max_length=MAX_CHAR_LENGTH)
    phone = models.BigIntegerField(default=0,null=True)
    created_time = models.FloatField(default=utils_time.get_timestamp())

    def serialize(self):
        data = {
            "id":self.id,
            "driver":self.driver,
            "license":self.license,
            "phone":self.phone,
            "created_time":self.created_time
        }
        return data   
    
class Pay(models.Model):
    id = models.BigAutoField(primary_key=True)
    method = models.CharField(max_length=MAX_CHAR_LENGTH)
    created_time = models.FloatField(default=utils_time.get_timestamp())

    def serialize(self):
        data = {
            "id":self.id,
            "method":self.method,
            "created_time":self.created_time
        }
        return data

class Site2owner(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    owner = models.CharField(max_length=MAX_CHAR_LENGTH)
    phone = models.BigIntegerField(default=0)
    created_time = models.FloatField(default=utils_time.get_timestamp())

    def serialize(self):
        data = {
            "id":self.id,
            "name":self.name,
            "owner":self.owner,
            "phone":self.phone,
            "created_time":self.created_time
        }
        return data