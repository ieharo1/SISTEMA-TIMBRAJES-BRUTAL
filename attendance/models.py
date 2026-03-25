from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Office(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    timezone = models.CharField(max_length=64, default='UTC')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='employees')
    employee_code = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=120)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.employee_code} - {self.user.get_full_name() or self.user.username}"


class Shift(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.PositiveIntegerField(default=60)
    overtime_threshold_minutes = models.PositiveIntegerField(default=480)

    class Meta:
        ordering = ['office__name', 'name']

    def __str__(self):
        return f"{self.office.name} - {self.name}"


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='records')
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, related_name='records')
    clock_in = models.DateTimeField(default=timezone.now)
    clock_out = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clock_in']

    def __str__(self):
        return f"{self.employee} - {self.clock_in:%Y-%m-%d}"

    @property
    def is_open(self):
        return self.clock_out is None

    @property
    def worked_minutes(self):
        end = self.clock_out or timezone.now()
        delta = end - self.clock_in
        minutes = max(int(delta.total_seconds() // 60) - self.shift.break_minutes, 0)
        return minutes

    @property
    def overtime_minutes(self):
        return max(self.worked_minutes - self.shift.overtime_threshold_minutes, 0)

    @property
    def worked_hours_decimal(self):
        return round(self.worked_minutes / 60, 2)

    @property
    def overtime_hours_decimal(self):
        return round(self.overtime_minutes / 60, 2)

    @property
    def regular_pay(self):
        regular_minutes = min(self.worked_minutes, self.shift.overtime_threshold_minutes)
        return round((regular_minutes / 60) * float(self.employee.hourly_rate), 2)

    @property
    def overtime_pay(self):
        return round((self.overtime_minutes / 60) * float(self.employee.hourly_rate) * 1.5, 2)
