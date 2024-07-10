import json
from django.http import HttpRequest
from parameter.models import Site,Goods,Vehicle,Pay,Site2owner
from django.contrib.auth.hashers import check_password
from utils.utils_request import BAD_METHOD, request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from utils.utils_jwt import generate_jwt_token
from utils.utils_format import check_string_format
from utils.constants import OFFLINE,CANCELED
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from utils.constants import SITE_TYPE,START,END


# Create your views here.
@CheckRequire
def start_site(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    name = require(body,"name","string",err_msg="Missing or error type of [name]")
    manager = require(body,"manager","string",err_msg="Missing or error type of [manager]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    try:
        phone = int(phone_str)
    except ValueError:
        return request_failed(code=1,info="Phone number must be in numeric format",status_code=400)
    Newsite = Site.objects.create(name=name,manager=manager,manager_phone=phone,type=START,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_start_site(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    site_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    site = Site.objects.filter(id=site_id).first()
    if not site:
        return request_failed(code=1,info="Site does not exist",status_code=404)
    Site.objects.delete(site)
    return request_success()

@CheckRequire
def start_site_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    site_list = Site.objects.filter(type=START).order_by("-created_time")
    paginator = Paginator(site_list,per_page)
    site_page = paginator.get_page(page)
    return_data = [site.serialize() for site in site_page]
    return request_success({"start_sites":return_data})

# Create your views here.
@CheckRequire
def end_site(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    name = require(body,"name","string",err_msg="Missing or error type of [name]")
    manager = require(body,"manager","string",err_msg="Missing or error type of [manager]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    try:
        phone = int(phone_str)
    except ValueError:
        return request_failed(code=1,info="Phone number must be in numeric format",status_code=400)
    Newsite = Site.objects.create(name=name,manager=manager,manager_phone=phone,type=END,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_end_site(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    site_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    site = Site.objects.filter(id=site_id).first()
    if not site:
        return request_failed(code=1,info="Site does not exist",status_code=404)
    Site.objects.delete(site)
    return request_success()

@CheckRequire
def end_site_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    site_list = Site.objects.filter(type=END).order_by("-created_time")
    paginator = Paginator(site_list,per_page)
    site_page = paginator.get_page(page)
    return_data = [site.serialize() for site in site_page]
    return request_success({"start_sites":return_data})


@CheckRequire
def new_goods(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    goods_name = require(body,"name","string",err_msg="Missing or error type of [name]")
    Newgoods = Goods.objects.create(name=goods_name,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_goods(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    goods_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    goods = Goods.objects.filter(id=goods_id).first()
    if not goods:
        return request_failed(code=1,info="Goods does not exist",status_code=404)
    Goods.objects.delete(goods)
    return request_success()

@CheckRequire
def goods_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    goods_list = Goods.objects.all().order_by("-created_time")
    paginator = Paginator(goods_list,per_page)
    goods_page = paginator.get_page(page)
    return_data = [goods.serialize() for goods in goods_page]
    return request_success({"goods":return_data})

@CheckRequire
def new_vehicle(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    Newlicense = require(body,"license","string",err_msg="Missing or error type of [license]")
    Newdriver = require(body,"driver","string",err_msg="Missing or error type of [driver]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    Newphone = int(phone_str)
    Newvehicle = Vehicle.objects.create(license=Newlicense,driver=Newdriver,phone=Newphone,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_vehicle(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    vehicle_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
    if not vehicle:
        return request_failed(code=1,info="Vehicle does not exist",status_code=404)
    Vehicle.objects.delete(vehicle)
    return request_success()

@CheckRequire
def vehicle_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    vehicle_list = Vehicle.objects.all().order_by("-created_time")
    paginator = Paginator(vehicle_list,per_page)
    vehicle_page = paginator.get_page(page)
    return_data = [vehicle.serialize() for vehicle in vehicle_page]
    return request_success({"vehicle":return_data})

@CheckRequire
def new_site2owner(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8")) 
    name = require(body,"siteName","string",err_msg="Missing or error type of [siteName]")
    owner = require(body,"ownerName","string",err_msg="Missing or error type of [ownerName]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    try:
        phone = int(phone_str)
    except ValueError:
        return request_failed(code=1,info="Phone number must be in numeric format",status_code=400)
    Newsite2owner = Site2owner.objects.create(name=name,owner=owner,phone=phone,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_site2owner(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    site2owner_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    site2owner = Site2owner.objects.filter(id=site2owner_id).first()
    if not site2owner:
        return request_failed(code=1,info="Site2owner does not exist",status_code=404)
    Site2owner.objects.delete(site2owner)
    return request_success()

@CheckRequire
def site2owner_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    site2owner_list = Site2owner.objects.all().order_by("-created_time")
    paginator = Paginator(site2owner_list,per_page)
    site2owner_page = paginator.get_page(page)
    return_data = [site2owner.serialize() for site2owner in site2owner_page]
    return request_success({"site2owner":return_data})

@CheckRequire
def owner2site(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    ownerName = req.GET.get('ownerName', None)
    if not ownerName:
        return request_failed(code=1,info="Owner name not found in the request",status_code=400)
    site2owner_list = Site2owner.objects.filter(owner=ownerName).order_by("-created_time")
    paginator = Paginator(site2owner_list,per_page)
    site2owner_page = paginator.get_page(page)
    return_data = [site2owner.serialize() for site2owner in site2owner_page]
    return request_success({"site2owner":return_data})

@CheckRequire
def site2owner(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    id = req.GET.get('id', None)
    if not id:
        return request_failed(code=1,info="Site2owner id not found in the request",status_code=400)
    site2owner = Site2owner.objects.filter(id=id).first()
    return request_success(site2owner.serialize())

@CheckRequire
def new_pay(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    method = require(body,"method","string",err_msg="Missing or error type of [method]")
    Newpay = Pay.objects.create(method=method,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_pay(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    pay_id = require(body,"id","int",err_msg="Missing or error type of [id]")
    pay = Pay.objects.filter(id=pay_id).first()
    if not pay:
        return request_failed(code=1,info="Pay does not exist",status_code=404)
    Pay.objects.delete(pay)
    return request_success()

@CheckRequire
def pay_list(req:HttpRequest,per_page,page):
    failure_response, user = get_user_from_request(req,'GET')
    if failure_response:
        return failure_response
    pay_list = Pay.objects.all().order_by("-created_time")
    paginator = Paginator(pay_list,per_page)
    pay_page = paginator.get_page(page)
    return_data = [pay.serialize() for pay in pay_page]
    return request_success({"pay":return_data})