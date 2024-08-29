from django.urls import path
import user.views as views
urlpatterns = [
    path('login_password', views.login_password, name='login_password'),
    path('signup', views.signup, name='signup'),
    # path('jwt',views.refresh_access_token, name='refresh_token'),
    path('logout',views.logout, name='logout'),
    path('cancel',views.cancel, name='cancel'),
    path('info',views.info, name='info'),
    path('change_password',views.change_password, name='change_password'),
    path('change_username',views.change_username, name='change_username')

]