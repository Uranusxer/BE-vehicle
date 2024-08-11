from django.urls import path
import parameter.views as views

urlpatterns = [
    path('start_site', views.start_site, name='start_site'),
    path('start_site_list/<int:per_page>/<int:page>', views.start_site_list, name='start_site_list'),
    path('end_site', views.end_site, name='end_site'),
    path('end_site_list/<int:per_page>/<int:page>', views.end_site_list, name='end_site_list'),
    path('del_site/<int:site_id>', views.del_site, name='del_site'),
    path('change_site', views.change_site, name='change_site'),

    path('project', views.project, name='project'),
    path('del_project/<int:project_id>', views.del_project, name='del_project'),
    path('project_list/<int:per_page>/<int:page>', views.project_list, name='project_list'),
    path('change_project', views.change_project, name='change_project'),
    path('owner2project/<int:per_page>/<int:page>', views.owner2project, name='owner2project'),


    path('new_goods', views.new_goods, name='new_goods'),
    path('del_goods/<int:goods_id>', views.del_goods, name='del_goods'),
    path('goods_list/<int:per_page>/<int:page>', views.goods_list, name='goods_list'),
    path('change_goods', views.change_goods, name='change_goods'),


    path('new_vehicle', views.new_vehicle, name='new_vehicle'),
    path('del_vehicle/<int:vehicle_id>', views.del_vehicle, name='del_vehicle'),
    path('vehicle_list/<int:per_page>/<int:page>', views.vehicle_list, name='vehicle_list'),
    path('change_vehicle', views.change_vehicle, name='change_vehicle'),


    path('new_pay', views.new_pay, name='new_pay'),
    path('del_pay/<int:pay_id>', views.del_pay, name='del_pay'),
    path('pay_list/<int:per_page>/<int:page>', views.pay_list, name='pay_list'),
    path('change_pay', views.change_pay, name='change_pay'),


    path('owner_list/<int:per_page>/<int:page>', views.owner_list,name='owner_list')
]