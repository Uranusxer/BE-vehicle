from django.urls import path
import parameter.views as views

urlpatterns = [
    path('start_site', views.start_site, name='start_site'),
    path('del_start_site/<int:site_id>', views.del_start_site, name='del_start_site'),
    path('start_site_list/<int:per_page>/<int:page>', views.start_site_list, name='start_site_list'),
    
    path('end_site', views.end_site, name='end_site'),
    path('del_end_site/<int:site_id>', views.del_end_site, name='del_end_site'),
    path('end_site_list/<int:per_page>/<int:page>', views.end_site_list, name='end_site_list'),

    path('new_goods', views.new_goods, name='new_goods'),
    path('del_goods/<int:goods_id>', views.del_goods, name='del_goods'),
    path('goods_list/<int:per_page>/<int:page>', views.goods_list, name='goods_list'),

    path('new_vehicle', views.new_vehicle, name='new_vehicle'),
    path('del_vehicle/<int:vehicle_id>', views.del_vehicle, name='del_vehicle'),
    path('vehicle_list/<int:per_page>/<int:page>', views.vehicle_list, name='vehicle_list'),

    path('new_site2owner', views.new_site2owner, name='new_site2owner'),
    path('del_site2owner/<int:site2owner_id>', views.del_site2owner, name='del_site2owner'),
    path('site2owner_list/<int:per_page>/<int:page>', views.site2owner_list, name='site2owner_list'),
    path('owner2site/<int:per_page>/<int:page>', views.owner2site, name='owner2site'),
    path('site2owner', views.site2owner, name='site2owner_detail'),

    path('new_pay', views.new_pay, name='new_pay'),
    path('del_pay/<int:pay_id>', views.del_pay, name='del_pay'),
    path('pay_list/<int:per_page>/<int:page>', views.pay_list, name='pay_list'),
]