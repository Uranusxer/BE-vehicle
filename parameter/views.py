import json
from django.http import HttpRequest
from parameter.models import Site,Goods,Vehicle,Pay,Project
from item.models import Item
from utils.utils_request import request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from utils.constants import START,END


# Create your views here.
@CheckRequire
def start_site(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
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
def start_site_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    ownerName = req.GET.get('ownerName', None)
    project_id = req.GET.get('project_id', None)
    site_list = Site.objects.filter(type=START,if_delete=False).order_by("-created_time")
    if ownerName:
        project_list = Project.objects.filter(owner=ownerName,if_delete=False).order_by("-created_time")
    if project_id:
        project_list = Project.objects.filter(id=project_id,if_delete=False)
    if ownerName or project_id:
        project_ids = project_list.values_list('id', flat=True)
        item_list = Item.objects.filter(project_id__in=project_ids,if_delete=False)  # Filter sites based on project IDs
        siteid_list = [item.startsite_id for item in item_list]
        site_list = Site.objects.filter(id__in=siteid_list, type=START, if_delete=False).order_by("-created_time")

    paginator = Paginator(site_list,per_page)
    site_page = paginator.get_page(page)
    return_data = [site.serialize() for site in site_page]
    total_pages = paginator.num_pages
    return request_success({"start_sites":return_data,"total_pages":total_pages})

# Create your views here.
@CheckRequire
def end_site(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
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
def end_site_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    ownerName = req.GET.get('ownerName', None)
    project_id = req.GET.get('project_id', None)
    site_list = Site.objects.filter(type=END,if_delete=False).order_by("-created_time")
    if ownerName:
        project_list = Project.objects.filter(owner=ownerName,if_delete=False).order_by("-created_time")
    if project_id:
        project_list = Project.objects.filter(id=project_id,if_delete=False)

    if ownerName or project_id:
        project_ids = project_list.values_list('id', flat=True)
        item_list = Item.objects.filter(project_id__in=project_ids,if_delete=False)  # Filter sites based on project IDs
        siteid_list = [item.endsite_id for item in item_list]
        site_list = Site.objects.filter(id__in=siteid_list, type=END, if_delete=False).order_by("-created_time")

    paginator = Paginator(site_list,per_page)
    site_page = paginator.get_page(page)
    return_data = [site.serialize() for site in site_page]
    total_pages = paginator.num_pages
    return request_success({"end_sites":return_data,"total_pages":total_pages})


@CheckRequire
def del_site(req:HttpRequest,site_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    site = Site.objects.filter(id=site_id).first()
    if not site:
        return request_failed(code=1,info="Site does not exist",status_code=404)
    site.if_delete=True
    site.save()
    return request_success()


@CheckRequire
def change_site(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    site_id = require(body,"site_id","int",err_msg="Missing or error type of [site_id]")
    site = Site.objects.filter(id=site_id).first()
    if not site:
        return request_failed(code=1,info="Site does not exist",status_code=404)
    try:
        name = require(body, "name", "string", err_msg="Missing or error type of [name]")
    except:
        name = None
    try:
        manager = require(body, "manager", "string", err_msg="Missing or error type of [manager]")
    except:
        manager = None
    try:
        manager_phone = require(body, "manager_phone", "string", err_msg="Missing or error type of [manager_phone]")
        manager_phone = int(manager_phone)
    except:
        manager_phone = None
    if name:
        site.name = name
    if manager:
        site.manager = manager
    if manager_phone:
        site.manager_phone = manager_phone
    site.save()
    return request_success()

@CheckRequire
def project(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    name = require(body,"name","string",err_msg="Missing or error type of [name]")
    owner = require(body,"owner","string",err_msg="Missing or error type of [owner]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    try:
        phone = int(phone_str)
    except ValueError:
        return request_failed(code=1,info="Phone number must be in numeric format",status_code=400)
    Newproject = Project.objects.create(name=name,owner=owner,owner_phone=phone,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_project(req:HttpRequest,project_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return request_failed(code=1,info="Project does not exist",status_code=404)
    project.if_delete=True
    project.save()
    return request_success()

@CheckRequire
def project_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    owner = req.GET.get('owner', None)
    project_list = Project.objects.filter(if_delete=False).order_by("-created_time")
    if owner:
        project_list = project_list.filter(owner=owner)
    paginator = Paginator(project_list,per_page)
    project_page = paginator.get_page(page)
    return_data = [project.serialize() for project in project_page]
    total_pages = paginator.num_pages
    return request_success({"projects":return_data,"total_pages":total_pages})

@CheckRequire
def change_project(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    project_id = require(body,"project_id","int",err_msg="Missing or error type of [project_id]")
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return request_failed(code=1,info="Project does not exist",status_code=404)
    try:
        name = require(body, "name", "string", err_msg="Missing or error type of [name]")
    except:
        name = None
    try:
        owner = require(body, "owner", "string", err_msg="Missing or error type of [owner]")
    except:
        owner = None
    try:
        owner_phone = require(body, "owner_phone", "string", err_msg="Missing or error type of [owner_phone]")
        owner_phone = int(owner_phone)
    except:
        owner_phone = None
    if name:
        project.name = name
    if owner:
        project.owner = owner
    if owner_phone:
        project.owner_phone = owner_phone
    project.save()
    return request_success()

@CheckRequire
def owner2project(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    ownerName = req.GET.get('ownerName', None)
    if not ownerName:
        project_list = Project.objects.filter(if_delete=False).order_by("-created_time")
    else:
        project_list = Project.objects.filter(owner=ownerName,if_delete=False).order_by("-created_time")
    paginator = Paginator(project_list,per_page)
    current_page = paginator.get_page(page)
    return_data = [item.serialize() for item in current_page]
    total_pages = paginator.num_pages
    return request_success({"project":return_data,"total_pages":total_pages})

@CheckRequire
def new_goods(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    goods_name = require(body,"name","string",err_msg="Missing or error type of [name]")
    Newgoods = Goods.objects.create(name=goods_name,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_goods(req:HttpRequest,goods_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    goods = Goods.objects.filter(id=goods_id).first()
    if not goods:
        return request_failed(code=1,info="Goods does not exist",status_code=404)
    goods.if_delete=True
    goods.save()
    return request_success()

@CheckRequire
def goods_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    goods_list = Goods.objects.filter(if_delete=False).order_by("-created_time")
    paginator = Paginator(goods_list,per_page)
    goods_page = paginator.get_page(page)
    return_data = [goods.serialize() for goods in goods_page]
    total_pages = paginator.num_pages
    return request_success({"goods":return_data,"total_pages":total_pages})

@CheckRequire
def change_goods(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    goods_id = require(body,"goods_id","int",err_msg="Missing or error type of [goods_id]")
    goods = Goods.objects.filter(id=goods_id).first()
    if not goods:
        return request_failed(code=1,info="Goods does not exist",status_code=404)
    try:
        name = require(body, "name", "string", err_msg="Missing or error type of [name]")
    except:
        name = None
    if name:
        goods.name = name
    goods.save()
    return request_success()


@CheckRequire
def new_vehicle(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    Newlicense = require(body,"license","string",err_msg="Missing or error type of [license]")
    Newdriver = require(body,"driver","string",err_msg="Missing or error type of [driver]")
    phone_str = require(body,"phone","string",err_msg="Missing or error type of [phone]")
    Newphone = int(phone_str)
    Newvehicle = Vehicle.objects.create(license=Newlicense,driver=Newdriver,phone=Newphone,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_vehicle(req:HttpRequest,vehicle_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
    if not vehicle:
        return request_failed(code=1,info="Vehicle does not exist",status_code=404)
    vehicle.if_delete=True
    vehicle.save()
    return request_success()

@CheckRequire
def vehicle_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    vehicle_list = Vehicle.objects.filter(if_delete=False).order_by("-created_time")
    paginator = Paginator(vehicle_list,per_page)
    vehicle_page = paginator.get_page(page)
    return_data = [vehicle.serialize() for vehicle in vehicle_page]
    total_pages = paginator.num_pages
    return request_success({"vehicle":return_data,"total_pages":total_pages})

@CheckRequire
def change_vehicle(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    vehicle_id = require(body,"vehicle_id","int",err_msg="Missing or error type of [vehicle_id]")
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
    if not vehicle:
        return request_failed(code=1,info="Vehicle does not exist",status_code=404)
    try:
        driver = require(body, "driver", "string", err_msg="Missing or error type of [driver]")
    except:
        driver = None
    try:
        license = require(body, "license", "string", err_msg="Missing or error type of [license]")
    except:
        license = None
    try:
        phone = require(body, "phone", "string", err_msg="Missing or error type of [phone]")
        phone = int(phone)
    except:
        phone = None
    if driver:
        vehicle.driver = driver
    if license:
        vehicle.license = license
    if phone:
        vehicle.phone = phone
    vehicle.save()
    return request_success()


@CheckRequire
def new_pay(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    method = require(body,"method","string",err_msg="Missing or error type of [method]")
    Newpay = Pay.objects.create(method=method,created_time=get_timestamp())
    return request_success()

@CheckRequire
def del_pay(req:HttpRequest,pay_id):
    # failure_response, user = get_user_from_request(req,'DELETE')
    # if failure_response:
    #     return failure_response
    pay = Pay.objects.filter(id=pay_id).first()
    if not pay:
        return request_failed(code=1,info="Pay does not exist",status_code=404)
    pay.if_delete=True
    pay.save()
    return request_success()

@CheckRequire
def pay_list(req:HttpRequest,per_page,page):
    # failure_response, user = get_user_from_request(req,'GET')
    # if failure_response:
    #     return failure_response
    pay_list = Pay.objects.filter(if_delete=False).order_by("-created_time")
    paginator = Paginator(pay_list,per_page)
    pay_page = paginator.get_page(page)
    return_data = [pay.serialize() for pay in pay_page]
    total_pages = paginator.num_pages
    return request_success({"pay":return_data,"total_pages":total_pages})

@CheckRequire
def change_pay(req:HttpRequest):
    # failure_response, user = get_user_from_request(req,'POST')
    # if failure_response:
    #     return failure_response
    body = json.loads(req.body.decode("utf-8"))
    pay_id = require(body,"pay_id","int",err_msg="Missing or error type of [pay_id]")
    pay = Pay.objects.filter(id=pay_id).first()
    if not pay:
        return request_failed(code=1,info="Pay does not exist",status_code=404)
    try:
        method = require(body, "method", "string", err_msg="Missing or error type of [method]")
    except:
        method = None
    if method:
        pay.method = method
    pay.save()
    return request_success()

@CheckRequire
def owner_list(req: HttpRequest, per_page, page):
    # failure_response, user = get_user_from_request(req, 'POST')
    # if failure_response:
    #     return failure_response

    # 获取所有未删除的sites, 然后提取所有的不重复的owners
    owner_list = Project.objects.filter(if_delete=False).values_list("owner", flat=True).distinct().order_by("owner")
    # 过滤掉为None的项
    owner_list = [owner for owner in owner_list if owner is not None]
    # 分页处理
    paginator = Paginator(owner_list, per_page)
    owner_page = paginator.get_page(page)
    return_data = list(owner_page)
    total_pages = paginator.num_pages
    return request_success({"owner_list": return_data, "total_pages": total_pages})