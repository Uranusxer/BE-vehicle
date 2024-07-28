from django.urls import path
import finance.views as views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('advance', views.advance, name='advance'),
    path('del_advance/<int:advance_id>', views.del_advance, name='del_advance'),
    path('advance_list/<int:per_page>/<int:page>', views.advance_list, name='advance_list'),
    path('change_advance', views.change_advance, name='change_advance')
]