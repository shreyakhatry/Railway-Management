from django.contrib import admin
from dataaccess.models import (
    Ticket,
    Train,
    Station,
    Route
)
# Register your models here.

admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Ticket)