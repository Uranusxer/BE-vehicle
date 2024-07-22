from django.shortcuts import render
from django.http import HttpRequest
from item.models import Item
from utils.utils_request import BAD_METHOD, request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from utils.constants import START,END
import json

@CheckRequire
def transport_item(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    startsite_id = require(body,"startsite_id","int",err_msg="Missing or error type of [startsite_id]")
    endsite_id = require(body,"endsite_id","int",err_msg="Missing or error type of [endsite_id]")
    vehicle_id  = require(body,"vehicle_id","int",err_msg="Missing or error type of [vehicle_id]")
    goods_id = require(body,"goods_id","int",err_msg="Missing or error type of [goods_id]")
    start_date = require(body,"start_date","string",err_msg="Missing or error type of [start_date]")
    end_date = require(body,"end_date","string",err_msg="Missing or error type of [end_date]")
    Newitem = Item.objects.create(startsite_id=startsite_id,endsite_id=endsite_id,vehicle_id=vehicle_id,goods_id=goods_id,start_date=start_date,end_date=end_date,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_item(req:HttpRequest,item_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    item = Item.objects.filter(id=item_id).first()
    if not item:
        return request_failed(code=1,info="Item does not exist",status_code=404)
    item.if_delete=True
    return request_success()

@CheckRequire
def item_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    item_list = Item.objects.filter(if_delete=False).order_by("-created_time")
    paginator = Paginator(item_list,per_page)
    item_page = paginator.get_page(page)
    return_data = [item.serialize() for item in item_page]
    total_pages = paginator.num_pages
    return request_success({"items":return_data,"total_pages":total_pages})

@CheckRequire
def item_price(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    item_id = require(body,"item_id  ","int",err_msg="Missing or error type of [item_id]")
    contractorPrice = require(body,"contractorPrice ","float",err_msg="Missing or error type of [contractorPrice]")
    startSubsidy = require(body,"startSubsidy ","float",err_msg="Missing or error type of [startSubsidy]")
    endSubsidy = require(body,"endSubsidy  ","float",err_msg="Missing or error type of [endSubsidy]")
    endPayment = require(body,"endPayment ","float",err_msg="Missing or error type of [endPayment]")
    driverPrice = require(body,"driverPrice ","float",err_msg="Missing or error type of [driverPrice]")
    unit = require(body,"unit ","string",err_msg="Missing or error type of [unit]")
    item = Item.objects.filter(id=item_id).first()
    if not item:
        return request_failed(code=1,info="Item does not exist",status_code=404)
    item.contractorPrice = contractorPrice
    item.startSubsidy = startSubsidy
    item.endSubsidy = endSubsidy
    item.endPayment = endPayment
    item.driverPrice = driverPrice
    item.unit = unit
    item.save()
    return request_success()