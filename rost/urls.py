from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'rost'

urlpatterns = [
    path('', home, name='home'),
    path('create_object/', create_object, name='create_object'),
    path('delete/<int:object_id>/', delete_object, name='delete_object'),
    path('edit/<int:object_id>/', edit_object, name='edit_object'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', me_view, name='me'),
    path('admin_home/', admin_home, name='admin_home'),  # Админ панель
    path('export-admin-excel/', export_admin_excel, name='export_admin_excel'),
    path('import-admin-excel/', import_admin_excel, name='import_admin_excel'),
]
