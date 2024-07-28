from django.shortcuts import render
from django.http import HttpRequest
from item.models import Item
from parameter.models import Vehicle
from utils.utils_request import BAD_METHOD, request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from finance.models import Advance
from utils.constants import START,END
import json
from django.http import JsonResponse

@CheckRequire
def advance(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    vehicle_id  = require(body,"vehicle_id","int",err_msg="Missing or error type of [vehicle_id]")
    amount  = require(body,"amount","int",err_msg="Missing or error type of [amount]")
    advance_time  = require(body,"advance_time","string",err_msg="Missing or error type of [advance_time]")
    Newadvance = Advance.objects.create(vehicle_id=vehicle_id,amount=amount,advance_time=advance_time,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_advance(req:HttpRequest,advance_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    advance = Advance.objects.filter(id=advance_id,if_delete=False).first()
    if not advance:
        return request_failed(code=1,info="Advance does not exist",status_code=404)
    advance.if_delete=True
    advance.save()
    return request_success()

@CheckRequire
def advance_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    driver = req.GET.get('driver',None)

    advances = Advance.objects.all()
    if driver is not None:
        vehicle_ids = Vehicle.objects.filter(driver=driver).values_list('id', flat=True)
        advances = advances.filter(vehicle_id__in=vehicle_ids)
   
    paginator = Paginator(advances, per_page)
    current_page = paginator.get_page(page)
    total_pages = paginator.num_pages
    return_data = [advance.serialize() for advance in current_page]
    return request_success({"advances":return_data,"total_pages":total_pages})

@CheckRequire
def change_advance(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    advance_id = require(body,"advance_id","int",err_msg="Missing or error type of [advance_id]")
    advance = Advance.objects.filter(id=pay_id).first()
    if not advance:
        return request_failed(code=1,info="Advance does not exist",status_code=404)
    try:
        vehicle_id = require(body, "vehicle_id", "int", err_msg="Missing or error type of [vehicle_id]")
    except:
        vehicle_id = None
    try:
        amount = require(body, "amount", "int", err_msg="Missing or error type of [amount]")
    except:
        amount = None
    try:
        advance_time = require(body, "advance_time", "string", err_msg="Missing or error type of [advance_time]")
    except:
        advance_time = None
    if vehicle_id:
        advance.vehicle_id = vehicle_id
    if amount:
        advance.amount = amount
    if advance_time:
        advance.advance_time = advance_time
    advance.save()
    return request_success()

