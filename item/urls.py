from django.urls import path
import item.views as views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('transport_item', views.transport_item, name='transport_item'),
    path('del_item/<int:item_id>', views.del_item, name='del_item'),
    path('item_list/<int:per_page>/<int:page>', views.item_list, name='item_list'),
    path('item_price', views.item_price, name='item_price')
]