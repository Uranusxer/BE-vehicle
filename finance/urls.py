from django.urls import path
import finance.views as views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('advance', views.advance, name='advance'),
    path('del_advance/<int:advance_id>', views.del_advance, name='del_advance'),
    path('advance_list/<int:per_page>/<int:page>', views.advance_list, name='advance_list'),
    path('change_advance', views.change_advance, name='change_advance'),
    path('driver_excel', views.driver_excel, name='driver_excel'),
    path('driver_excel_pdf', views.driver_excel_pdf, name='driver_excel_pdf'),
    path('total_amount', views.total_amount, name='total_amount'),
    path('search4advance/<int:per_page>/<int:page>', views.search4advance, name='search4advance'),
    
    path('payment', views.payment, name='payment'),
    path('del_payment/<int:payment_id>', views.del_payment, name='del_payment'),
    path('payment_list/<int:per_page>/<int:page>', views.payment_list, name='payment_list'),
    path('change_payment', views.change_payment, name='change_payment'),
    path('search4payment/<int:per_page>/<int:page>', views.search4payment, name='search4payment')


]