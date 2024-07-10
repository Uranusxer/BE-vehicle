from django.shortcuts import render
from utils.utils_require import CheckRequire, require
from django.http import HttpRequest
from utils.utils_request import BAD_METHOD, request_failed, request_success
import json
from user.models import User,get_user_from_request
from django.contrib.auth.hashers import check_password
from utils.utils_jwt import generate_jwt_token
from utils.utils_format import check_string_format
from utils.utils_time import get_timestamp
from utils.constants import OFFLINE

# Create your views here.
# 登录时，后端向前端返回用户基本信息
@CheckRequire
def login(req: HttpRequest):
    if req.method != "POST":
        return BAD_METHOD
    body = json.loads(req.body.decode("utf-8"))
    username = require(body, "username", "string", err_msg="Missing or error type of [username]")
    password = require(body, "password", "string", err_msg="Missing or error type of [password]")
    user = User.objects.filter(name=username).first()
    if user:
        if check_password(password, user.password):
            user.set_login()
            access_token = generate_jwt_token(username)
            return_data = {
                "token":access_token,
                "username":user.name,
                "phone":user.phone,
                "register_time":user.register_time,
                "login_time":user.login_time,
            }
            return request_success(return_data)
        else:
            return request_failed(code=2,info="Wrong password",status_code=401)
    else:
        #用户不存在
        return request_failed(code=-2,info="User ID Unauthorized.", status_code=404)

@CheckRequire
def signup(req:HttpRequest): # 注册
    if req.method != "POST":
        return BAD_METHOD
    body = json.loads(req.body.decode("utf-8"))
    username = require(body, "username", "string", err_msg="Missing or error type of [username]")
    password = require(body, "password", "string", err_msg="Missing or error type of [password]")
    try:
        phone_str = require(body, "phone", "string", err_msg="Missing or error type of [phone]")
        phone = int(phone_str)
    except:
        phone = None
    register_time = get_timestamp()
    # 传入头像单独实现
    # 检查密码和姓名格式是否符合要求(仅由字符、数字构成，不包含空格等)
    if(check_string_format(username,30)== True and check_string_format(password,25) == True):
        user = User.objects.create(name=username,password=password,phone=phone,register_time=register_time)
        user.save() 
        return request_success({"userID":user.id})
    else:
        return request_failed(code=-4,info="Invalid format for the username or password.", status_code=400)

@CheckRequire
def logout(req: HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    user.status = OFFLINE
    return request_success()    

@CheckRequire
def cancel(req: HttpRequest):
    failure_response, user = get_user_from_request(req,'DELETE')
    if failure_response:
        return failure_response
    # TODO:注销用户
    user.delete()
    return request_success()

@CheckRequire
def change_password(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'POST')
    if failure_response:
        return failure_response
    body = json.loads(req.body.decode("utf-8"))
    oldPassword = require(body, "oldPassword", "string", err_msg="Missing or error type of [oldPassword]")
    newPassword = require(body, "newPassword", "string", err_msg="Missing or error type of [newPassword]")
    if check_password(oldPassword, user.password):
        user.password = newPassword
        user.save()
        return request_success()
    return request_failed(code=2,info="Wrong password",status_code=401)

@CheckRequire
def info(req:HttpRequest):
    failure_response, user = get_user_from_request(req,'GET','POST')
    if failure_response:
        return failure_response
    if req.method == 'POST':
        body = json.loads(req.body.decode("utf-8"))
        try:
            username = require(body, "username", "string", err_msg="Missing or error type of [username]")
        except:
            username = None
        try:
            phone_str = require(body, "phone", "string", err_msg="Missing or error type of [phone]")
            phont = int(phone_str)
        except:
            phone = None
        if username:
            user.name = username
        if phone:
            user.phone = phone
        user.save()
        return request_success()
    else:
        return_data = user.serialize()
        return_data['phone'] = user.phone
        return_data['register_time'] = user.register_time
        return request_success(return_data)