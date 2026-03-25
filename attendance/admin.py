from django.contrib import admin

from .models import AttendanceRecord, Employee, Office, Shift

admin.site.register(Office)
admin.site.register(Employee)
admin.site.register(Shift)
admin.site.register(AttendanceRecord)
