from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from attendance.models import AttendanceRecord, Employee, Office, Shift


class Command(BaseCommand):
    help = 'Carga datos iniciales de demo'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.set_password('admin123')
            admin.is_superuser = True
            admin.is_staff = True
            admin.first_name = 'Admin'
            admin.last_name = 'Sistema'
            admin.save()

        office, _ = Office.objects.get_or_create(name='HQ Central', city='Quito', country='Ecuador', timezone='America/Guayaquil')
        shift, _ = Shift.objects.get_or_create(
            office=office,
            name='Oficina Diurna',
            defaults={'start_time': '08:00', 'end_time': '17:00', 'break_minutes': 60, 'overtime_threshold_minutes': 480},
        )

        user, _ = User.objects.get_or_create(username='empleado.demo', defaults={'first_name': 'Empleado', 'last_name': 'Demo'})
        if not user.has_usable_password():
            user.set_password('demo12345')
            user.save()

        employee, _ = Employee.objects.get_or_create(
            user=user,
            defaults={
                'office': office,
                'employee_code': 'EMP-001',
                'position': 'Analista',
                'hourly_rate': 8.50,
                'is_active': True,
            },
        )

        if not AttendanceRecord.objects.filter(employee=employee).exists():
            in_time = timezone.now() - timezone.timedelta(hours=10)
            out_time = timezone.now() - timezone.timedelta(hours=1)
            AttendanceRecord.objects.create(employee=employee, shift=shift, clock_in=in_time, clock_out=out_time, notes='Turno de prueba')

        self.stdout.write(self.style.SUCCESS('Datos semilla verificados.'))
