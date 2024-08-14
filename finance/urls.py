from django.urls import path
import finance.views as views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('advance', views.advance, name='advance'),
    path('del_advance/<int:advance_id>', views.del_advance, name='del_advance'),
    path('advance_list/<int:per_page>/<int:page>', views.advance_list, name='advance_list'),
    path('change_advance', views.change_advance, name='change_advance'),
    path('driver_excel', views.driver_excel, name='driver_excel'),
    path('total_amount', views.total_amount, name='total_amount'),
    path('search4advance/<int:per_page>/<int:page>', views.search4advance, name='search4advance')

]