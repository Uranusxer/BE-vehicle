from django.shortcuts import render
from item.models import Item
from parameter.models import Site,Goods,Vehicle
from utils.utils_request import BAD_METHOD, request_failed, request_success
from utils.utils_require import CheckRequire, require
from utils.utils_time import get_timestamp
from django.core.paginator import Paginator
from user.models import User,get_user_from_request
from utils.constants import START,END
import json
from django.http import JsonResponse
from openpyxl import Workbook
import io
from datetime import datetime
from django.http import HttpRequest, HttpResponse
from openpyxl.styles import Alignment, Font, Border, Side
from django.db.models import Sum
import re

def num2cn(n):
    # 定义中文数字和单位
    cn_nums = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
    cn_units = ["", "拾", "佰", "仟"]
    cn_decimal_units = ["角", "分"]  # 一般只取两位小数

    # 将数字按小数点分开
    if isinstance(n, float):
        integer_part, decimal_part = str(n).split('.')
    else:
        integer_part, decimal_part = str(n), None

    # 处理整数部分
    int_result = "".join([
        cn_nums[int(digit)] + (cn_units[(len(integer_part) - i - 1) % 4] if digit != '0' else '')
        for i, digit in enumerate(integer_part)
    ])

    # 将整数部分的零零相连去掉，只保留一个零
    int_result = re.sub('零+', '零', int_result)
    if int_result.endswith('零'):
        int_result = int_result[:-1]

    # 处理小数部分
    if decimal_part:
        dec_result = ""
        for i in range(min(len(decimal_part), 2)):  # 一般只处理到分（两位小数）
            digit = int(decimal_part[i])
            if digit != 0:
                dec_result += cn_nums[digit] + cn_decimal_units[i]
            else:
                dec_result += cn_nums[digit]
        dec_result = re.sub('零+', '零', dec_result).rstrip('零')
    else:
        dec_result = ""

    # 将整数部分和小数部分组合起来
    if dec_result:
        return int_result + '点' + dec_result
    else:
        return int_result

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
        request_failed(code=1,info="Phone number must be in numeric format",status_code=400)
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

@CheckRequire
def item2excel(req: HttpRequest):
    # 从请求参数中获取数据
    body = json.loads(req.body.decode("utf-8"))
    item_ids = require(body, "item_ids", "list", err_msg="Missing or error type of [item_ids]")
    startsite_id = require(body, "startsite_id", "int", err_msg="Missing or error type of [startsite_id]")
    start_date = require(body, "start_date", "string", err_msg="Missing or error type of [start_date]")
    end_date = require(body, "end_date", "string", err_msg="Missing or error type of [end_date]")
    
    # 获取startsite对象并检查
    startsite = Site.objects.filter(id=startsite_id).first()
    if not startsite:
        return request_failed(code=3, info="startsite not found", status_code=404)
    
    # 转换日期格式，假设传入的日期格式为"2024-07-03T16:00:00.000Z"
    start_date = start_date.split('T')[0]
    end_date = end_date.split('T')[0]
    
    # 获取过滤的Item
    items = Item.objects.filter(id__in=item_ids, if_delete=False)
    
    # 创建Excel工作簿
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "宏途运输每月对账单"
    default_font = Font(size=12)
    def set_font_and_alignment(cell):
        cell.font = default_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    # 设置列宽
    column_widths = {
        'A': 5,    # 序号
        'B': 15,   # 起始日期
        'C': 15,   # 合并单元格"起始日期"
        'D': 20,   # 运输起点
        'E': 20,   # 合并单元格"运输起点"
        'F': 10,   # 终点工地
        'G': 15,   # 品类
        'H': 15,   # 合并单元格"品类"
        'I': 10,   # 数量
        'J': 10,   # 单位
        'K': 10,   # 单价
        'L': 15,   # 终点付费金额
        'M': 15,   # 起点补贴金额
        'N': 15    # 终点补贴金额
    }

    for col_letter, width in column_widths.items():
        sheet.column_dimensions[col_letter].width = width

    # 添加表头
    sheet.merge_cells('A1:N1')
    title_cell = sheet['A1']
    title_cell.value = "宏途运输每月对账单"
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    title_cell.font = Font(size=24, bold=True)


    # 固定的表头信息
    sheet.merge_cells('A2:C2')
    sheet.merge_cells('D2:F2')
    sheet.merge_cells('G2:H2')
    sheet.merge_cells('I2:N2')
    sheet.merge_cells('A3:C3')
    sheet.merge_cells('D3:F3')
    sheet.merge_cells('G3:H3')
    sheet.merge_cells('I3:N3')
    sheet.merge_cells('A4:C4')
    sheet.merge_cells('D4:F4')
    sheet.merge_cells('G4:H4')
    sheet.merge_cells('I4:N4')
    
    sheet['A2'] = "起 点 工 地 单 位 名 称"
    sheet['D2'] = startsite.name
    sheet['G2'] = "工 地 老 板 名 称"
    sheet['I2'] = startsite.owner
    sheet['A3'] = "对 账 起 始 日 期"
    sheet['D3'] = start_date
    sheet['G3'] = "对 账 截 止 日 期"
    sheet['I3'] = end_date
    sheet['A4'] = "运 输 单 位 名 称"
    sheet['D4'] = "八 达 通 渣 土 运 输 有 限 公 司"
    sheet['G4'] = "公 司 负 责 人"
    sheet['I4'] = "叶 家 荣 19859999999"
    
    for row in sheet['A2:N4']:
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.font = Font(bold=True)
    
    # 列标题
    headers = ["序号", "起始日期", "", "运输起点", "", "终点工地", "品类", "", "数量", "单位", "单价", "终点付费金额", "起点补贴金额", "终点补贴金额"]
    sheet.append(headers)
    
    current_row = sheet.max_row
    sheet.merge_cells(f'B{current_row}:C{current_row}')
    sheet.merge_cells(f'D{current_row}:E{current_row}')
    sheet.merge_cells(f'G{current_row}:H{current_row}')
    
    for cell in sheet[current_row]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    # 合并相同条件下的明细
    summary = items.values(
        'start_date',
        'start_spot',
        'unit',
        'contractorPrice',
        'goods_id',
        'endsite_id'
    ).annotate(
        quantity_sum=Sum('quantity'),
        end_payment_sum=Sum('endPayment'),
        start_subsidy_sum=Sum('startSubsidy'),
        end_subsidy_sum=Sum('endSubsidy')
    )
    
    total_amount = 0
    for idx, item in enumerate(summary, start=1):
        end_site = Site.objects.filter(id=item['endsite_id']).first()
        end_site_name = end_site.name if end_site else "无"
        
        goods = Goods.objects.filter(id=item['goods_id']).first()
        goods_name = goods.name if goods else "无"
        row = [
            idx,
            item['start_date'].split('T')[0],
            "",
            item['start_spot'],
            "",
            end_site_name,
            goods_name,
            "",
            item['quantity_sum'],
            item['unit'],
            item['contractorPrice'],
            item['end_payment_sum'],
            item['start_subsidy_sum'],
            item['end_subsidy_sum']
        ]
        # 将数据追加到sheet中，并合并相应的单元格
        sheet.append(row)
        current_row = sheet.max_row
        sheet.merge_cells(f'B{current_row}:C{current_row}')
        sheet.merge_cells(f'D{current_row}:E{current_row}')
        sheet.merge_cells(f'G{current_row}:H{current_row}')

        for cell in sheet[current_row]:
            cell.alignment = Alignment(horizontal='center', vertical='center')

        total_amount += item['quantity_sum'] * item['contractorPrice']

    # 合计行
    total_cn = num2cn(total_amount)
    sheet.append(["合 计", "", "", "-", "", "-", "", "-", sum(item['quantity_sum'] for item in summary), "-", "-", "-", "-", "-"])
    current_row = sheet.max_row
    sheet.merge_cells(f'A{current_row}:C{current_row}')
    sheet.merge_cells(f'D{current_row}:E{current_row}')
    sheet.merge_cells(f'G{current_row}:H{current_row}')
    for cell in sheet[current_row]:
        cell.alignment = Alignment(horizontal='center')
    sheet.append(["总 计 金 额", "", "", total_amount, "", "总 计 大 写  (金 额 )", "", "", total_cn])
    current_row = sheet.max_row
    sheet.merge_cells(f'A{current_row}:C{current_row}')
    sheet.merge_cells(f'D{current_row}:E{current_row}')
    sheet.merge_cells(f'F{current_row}:H{current_row}')
    sheet.merge_cells(f'I{current_row}:N{current_row}')
    for cell in sheet[current_row]:
        cell.alignment = Alignment(horizontal='center')
    
    
    # 运输品类合计
    headers = ["","","序号", "运输起点", "", "终点工地", "品类", "", "数量", "单位", "单价", "终点付费金额", "起点补贴金额", "终点补贴金额"]
    sheet.append(headers)

    current_row = sheet.max_row
    sheet.merge_cells(f'A{current_row}:B{current_row}')
    sheet.merge_cells(f'D{current_row}:E{current_row}')
    sheet.merge_cells(f'G{current_row}:H{current_row}')
    
    for cell in sheet[current_row]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    transport_summary = items.values(
        'start_spot',
        'contractorPrice',
        'unit',
        'goods_id',
        'endsite_id'
    ).annotate(
        quantity_sum=Sum('quantity'),
        end_payment_sum=Sum('endPayment'),
        start_subsidy_sum=Sum('startSubsidy'),
        end_subsidy_sum=Sum('endSubsidy')
    )
    row1 = sheet.max_row+1
    for idx, item in enumerate(transport_summary, start=1):
        end_site = Site.objects.filter(id=item['endsite_id']).first()
        end_site_name = end_site.name if end_site else "无"
        
        goods = Goods.objects.filter(id=item['goods_id']).first()
        goods_name = goods.name if goods else "无"
        row = [
            "",
            "",
            idx,
            item['start_spot'],
            "",
            end_site_name,
            goods_name,
            "",
            item['quantity_sum'],
            item['unit'],
            item['contractorPrice'],
            item['end_payment_sum'],
            item['start_subsidy_sum'],
            item['end_subsidy_sum']
        ]
        sheet.append(row)
        current_row = sheet.max_row
        sheet.merge_cells(f'A{current_row}:B{current_row}')
        sheet.merge_cells(f'D{current_row}:E{current_row}')
        sheet.merge_cells(f'G{current_row}:H{current_row}')

        for cell in sheet[current_row]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
    row2 = sheet.max_row
    sheet.merge_cells(start_row=row1, start_column=1, end_row=row2, end_column=2)
    cell = sheet.cell(row=row1, column=1)
    cell.value = "运 输 品 类 合 计"
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    
    sheet.append(["","","合计","-","","-","-","","-","-","-","-","-","-"])
    current_row = sheet.max_row
    sheet.merge_cells(f'A{current_row}:B{current_row}')
    sheet.merge_cells(f'D{current_row}:E{current_row}')
    sheet.merge_cells(f'G{current_row}:H{current_row}')
    for cell in sheet[current_row]:
        cell.alignment = Alignment(horizontal='center')

    # 工地负责人及固定信息
    sheet.append(["工 地 负 责 人（ 签 字 确 认 ) ：","","","","","运 输 单 位 负 责 人 (  签 字 确 认 ) ："])
    current_row = sheet.max_row
    sheet.merge_cells(f'A{current_row}:E{current_row}')
    sheet.merge_cells(f'F{current_row}:N{current_row}')

    
    sheet.append(["经 营 范 围 ： 本 公 司 承 拆 土 石 方 工 程 、渣 土 、 建 筑 垃 圾 运 输 、 砂 石 料 、 柴 油 配 送 等 。"])
    current_row = sheet.max_row
    for cell in sheet[current_row]:
        cell.font = Font(bold=True)
    sheet.append(["成 就 伙 伴 、 铸 造 品 牌 、 我 们 每 天 努 力 、 我 们 每 天 进 步 。宏 途 运 输 每 月 对 帐 单"])
    centered_row = sheet.max_row
    sheet.merge_cells(f'A{centered_row}:N{centered_row}')
    # 设置该行每个单元格居中对齐
    for cell in sheet[centered_row]:
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.font = Font(size=16,bold=True)

    # # 保存到本地
    for row in sheet.iter_rows():
        sheet.row_dimensions[row[0].row].height = 15
        for cell in row:
            if not cell.font:
                set_font_and_alignment(cell)
    sheet.row_dimensions[1].height = 25  # 设置第一行的行高
    sheet.row_dimensions[2].height = 25  # 设置第一行的行高
    sheet.row_dimensions[3].height = 25  # 设置第一行的行高
    sheet.row_dimensions[sheet.max_row].height = 22  # 设置第一行的行高
    sheet.row_dimensions[sheet.max_row-2].height = 30  # 设置第一行的行高
    # return request_success()
    # 保存到内存
    local_file_path = "/root/cheliangyunshu/BE-vehicle/test/test.xlsx"
    workbook.save(local_file_path)
    print(1)
    file_stream = io.BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)
    
    response = HttpResponse(file_stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment;filename=transport_statement.xlsx'
    return response