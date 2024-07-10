from django.urls import path
import user.views as views
urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    # path('jwt',views.refresh_access_token, name='refresh_token'),
    path('logout',views.logout, name='logout'),
    path('cancel',views.cancel, name='cancel'),
    path('info',views.info, name='info'),
    path('change_password',views.change_password, name='change_password')
]