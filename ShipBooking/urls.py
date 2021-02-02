from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='view_home'),
    path('admin_check', views.admincheck, name='admin_check'),
    path('new_user', views.new_user, name='new_user'),
    path('user_login', views.user_login, name='user_login'),
    path('add_ship', views.add_ship, name='add_ship'),
    # path('services', views.services,name='services'),
    path('add_route', views.add_route, name='add_route'),
    path('update_ship/<str:action>', views.update_ship, name='update_ship'),
    path('ajax/get_user_info', views.getUserInfo, name = 'get_user_info'),
    path('deleteship', views.delete_ship, name='delete_ship'),
    path('deleteroute', views.delete_route, name='delete_route'),
    path('booking/<str:name>', views.ship_booking, name='booking'),
    path('get_ships_info', views.get_ships_info, name='get_ships_info'),
    path('booktickets/<str:name>', views.book_tickets, name='book_tickets'),
    path('bookhistory/<str:name>', views.booking_history, name='booking_history'),
]
