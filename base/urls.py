from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account_transfer/', views.account_transfer, name='account_transfer'),
    path('import_accounts/', views.import_accounts, name='import_accounts'),
    path('send_money/', views.send_money, name='send_money'),

]
