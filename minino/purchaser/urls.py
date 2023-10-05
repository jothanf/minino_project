from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchaser_home, name='purchaser_home'),
    path('create_purchaser/', views.create_purches, name='create_purchaser'),
    path('signin/', views.signin, name='signin'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('all_purchases/', views.all_purchases, name='all_purchases'),
    path('search_by_user/', views.search_by_user, name='search_by_user'),
    path('purchases_by_user/<int:purchaser_id>/', views.purchases_by_user, name='purchases_by_user'),
    path('search_by_state/', views.search_by_state, name='search_by_state'),
]