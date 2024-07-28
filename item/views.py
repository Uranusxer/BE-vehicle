from django.shortcuts import render
from django.http import HttpRequest
from item.models import Item
from parameter.models import Site
from utils.utils_request import BAD_METHOD, request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from utils.constants import START,END
import json
from django.http import JsonResponse

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
    start_spot = require(body,"start_spot","string",err_msg="Missing or error type of [start_spot]")
    start_date = require(body,"start_date","string",err_msg="Missing or error type of [start_date]")
    end_date = require(body,"end_date","string",err_msg="Missing or error type of [end_date]")
    Newitem = Item.objects.create(startsite_id=startsite_id,endsite_id=endsite_id,vehicle_id=vehicle_id,goods_id=goods_id,start_date=start_date,end_date=end_date,created_time=get_timestamp(),start_spot=start_spot)
    return request_success()

@CheckRequire
def del_item(req:HttpRequest,item_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    item = Item.objects.filter(id=item_id,if_delete=False).first()
    if not item:
        return request_failed(code=1,info="Item does not exist",status_code=404)
    item.if_delete=True
    item.save()
    return request_success()

@CheckRequire
def change_item(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response

    body = json.loads(req.body.decode("utf-8"))
    item_id = require(body,"item_id","int",err_msg="Missing or error type of [item_id]")
    item = Item.objects.filter(id=item_id,if_delete=False).first()
    if not item:
        return request_failed(code=1,info="Item does not exist",status_code=404)
    try:
        startsite_id = require(body, "startsite_id", "int", err_msg="Missing or error type of [startsite_id]")
    except:
        startsite_id = None
    try:
        endsite_id = require(body, "endsite_id", "int", err_msg="Missing or error type of [endsite_id]")
    except:
        endsite_id = None
    try:
        vehicle_id = require(body, "vehicle_id", "int", err_msg="Missing or error type of [vehicle_id]")
    except:
        vehicle_id = None
    try:
        goods_id = require(body, "goods_id", "int", err_msg="Missing or error type of [goods_id]")
    except:
        goods_id = None
    try:
        start_date = require(body, "start_date", "string", err_msg="Missing or error type of [start_date]")
    except:
        start_date = None
    try:
        end_date = require(body, "end_date", "string", err_msg="Missing or error type of [end_date]")
    except:
        end_date = None
    try:
        unit = require(body, "unit", "string", err_msg="Missing or error type of [unit]")
    except:
        unit = None
    try:
        contractorPrice = require(body, "contractorPrice", "float", err_msg="Missing or error type of [contractorPrice]")
    except:
        contractorPrice = None
    try:
        startSubsidy = require(body, "startSubsidy", "float", err_msg="Missing or error type of [startSubsidy]")
    except:
        startSubsidy = None
    try:
        endSubsidy = require(body, "endSubsidy", "float", err_msg="Missing or error type of [endSubsidy]")
    except:
        endSubsidy = None
    try:
        endPayment = require(body, "endPayment", "float", err_msg="Missing or error type of [endPayment]")
    except:
        endPayment = None
    try:
        driverPrice = require(body, "driverPrice", "float", err_msg="Missing or error type of [driverPrice]")
    except:
        driverPrice = None
    try:
        start_spot = require(body, "start_spot", "string", err_msg="Missing or error type of [start_spot]")
    except:
        start_spot = None
    try:
        quantity = require(body, "quantity", "float", err_msg="Missing or error type of [quantity]")
    except:
        quantity = None

    if startsite_id:
        item.startsite_id = startsite_id
    if endsite_id:
        item.endsite_id = endsite_id
    if vehicle_id:
        item.vehicle_id = vehicle_id
    if goods_id:
        item.goods_id = goods_id
    if start_date:
        item.start_date = start_date
    if end_date:
        item.end_date = end_date
    if unit:
        item.unit = unit
    if contractorPrice:
        item.contractorPrice = contractorPrice
    if startSubsidy:
        item.startSubsidy = startSubsidy
    if endSubsidy:
        item.endSubsidy = endSubsidy
    if endPayment:
        item.endPayment = endPayment
    if driverPrice:
        item.driverPrice = driverPrice
    if start_spot:
        item.start_spot = start_spot
    if quantity:
        item.quantity = quantity
    item.save()
    return request_success()

@CheckRequire
def search4item(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    startsite_owner = req.GET.get('startsite_owner',None)
    endsite_owner = req.GET.get('endsite_owner',None)
    startsite_id = req.GET.get('startsite_id',None)
    endsite_id = req.GET.get('endsite_id',None)
    vehicle_id = req.GET.get('vehicle_id',None)
    goods_id = req.GET.get('goods_id',None)
    start_date = req.GET.get('start_date',None)
    end_date = req.GET.get('end_date',None)
    unit = req.GET.get('unit',None)

    items = Item.objects.all()
    if startsite_owner is not None:
        startsite_ids = Site.objects.filter(owner=startsite_owner,if_delete=False).values_list('id', flat=True)
        items = items.filter(startsite_id__in=startsite_ids)
    
    if endsite_owner is not None:
        endsite_ids = Site.objects.filter(owner=endsite_owner,if_delete=False).values_list('id', flat=True)
        items = items.filter(endsite_id__in=endsite_ids,if_delete=False)

    if startsite_id is not None:
        items = items.filter(startsite_id=startsite_id,if_delete=False)
    if endsite_id is not None:
        items = items.filter(endsite_id=endsite_id,if_delete=False)
    if vehicle_id is not None:
        items = items.filter(vehicle_id=vehicle_id,if_delete=False)
    if goods_id is not None:
        items = items.filter(goods_id=goods_id,if_delete=False)
    if start_date is not None:
        items = items.filter(start_date__gte=start_date)
    if end_date is not None:
        items = items.filter(end_date__lte=end_date)
    if unit is not None:
        items = items.filter(unit=unit,if_delete=False)
    paginator = Paginator(items, per_page)
    current_page = paginator.get_page(page)
    total_pages = paginator.num_pages
    return_data = [item.serialize() for item in current_page]
    total_amount = sum(item.driverPrice for item in current_page)
    return request_success({"items":return_data,"total_pages":total_pages,"total_amount":total_amount})

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
def item_price(req: HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))

    items = body.get('items', [])
    if not isinstance(items, list):
        return JsonResponse({"error": "Invalid data format, 'items' should be a list"}, status=400)

    response_data = {"updated_items": [], "errors": []}

    for item_data in items:
        try:
            item_id = require(item_data, "item_id", "int", err_msg="Missing or error type of [item_id]")
            try:
                contractorPrice = require(item_data, "contractorPrice", "float", err_msg="Missing or error type of [contractorPrice]")
            except:
                contractorPrice = None
            try:
                startSubsidy = require(item_data, "startSubsidy", "float", err_msg="Missing or error type of [startSubsidy]")
            except:
                startSubsidy = None
            try:
                endSubsidy = require(item_data, "endSubsidy", "float", err_msg="Missing or error type of [endSubsidy]")
            except:
                endSubsidy = None
            try:
                endPayment = require(item_data, "endPayment", "float", err_msg="Missing or error type of [endPayment]")
            except:
                endPayment = None
            try:
                driverPrice = require(item_data, "driverPrice", "float", err_msg="Missing or error type of [driverPrice]")
            except:
                driverPrice = None
            try:
                quantity = require(item_data, "quantity", "float", err_msg="Missing or error type of [quantity]")
            except:
                quantity = None
            try:
                unit = require(item_data, "unit", "string", err_msg="Missing or error type of [unit]")
            except:
                unit = None

            item = Item.objects.filter(id=item_id,if_delete=False).first()
            if not item:
                response_data["errors"].append({"item_id": item_id, "error": "Item does not exist"})
                continue
            if contractorPrice:
                item.contractorPrice = contractorPrice
            if startSubsidy:
                item.startSubsidy = startSubsidy
            if endSubsidy:
                item.endSubsidy = endSubsidy
            if endPayment:
                item.endPayment = endPayment
            if driverPrice:
                item.driverPrice = driverPrice
            if quantity:
                item.quantity = quantity
            if unit:
                item.unit = unit
            item.save()

            response_data["updated_items"].append(item_id)
        
        except Exception as e:
            response_data["errors"].append({
                "item_data": item_data,
                "error": str(e)
            })
    
    if response_data["errors"]:
        return request_success()
    else:
        return JsonResponse(response_data, status=200)