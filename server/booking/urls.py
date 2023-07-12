from django.urls import re_path, path

from booking import views

urlpatterns = [
    re_path(r'^trains/(?P<stn_codes>[\w-]+)/(?P<doj>[\w-]+)$',views.get_train_details),
    re_path(r'^ticket/(?P<train_number>[\d]+)/$',views.book_ticket),
    re_path(r'^seatinfo/(?P<train_number>[\d]+)/$',views.seats_availabilty),
    re_path(r'^mybookings/$',views.my_bookings)
]