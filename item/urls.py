from django.urls import path
import item.views as views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('transport_item', views.transport_item, name='transport_item'),
    path('del_item/<int:item_id>', views.del_item, name='del_item'),
    path('item_list/<int:per_page>/<int:page>', views.item_list, name='item_list'),
    path('item_price', views.item_price, name='item_price'),
    path('change_item', views.change_item, name='change_item'),
    path('search4item/<int:per_page>/<int:page>', views.search4item, name='search4item'),
    path('start_excel',views.start_excel,name='start_excel'),
    path('start_excel_pdf', views.start_excel_pdf, name='start_excel_pdf'),
    path('end_excel',views.end_excel,name='end_excel'),
    path('end_excel_pdf', views.end_excel_pdf, name='end_excel_pdf'),
    path('detail_excel', views.detail_excel, name='detail_excel'),
    # path('item2excel',views.item2excel,name='item2excel')
]