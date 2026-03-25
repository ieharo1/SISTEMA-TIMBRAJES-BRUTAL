# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('country', models.CharField(max_length=120)),
                ('timezone', models.CharField(default='UTC', max_length=64)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_code', models.CharField(max_length=20, unique=True)),
                ('position', models.CharField(max_length=120)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='attendance.office')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['user__first_name', 'user__last_name']},
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('break_minutes', models.PositiveIntegerField(default=60)),
                ('overtime_threshold_minutes', models.PositiveIntegerField(default=480)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='attendance.office')),
            ],
            options={'ordering': ['office__name', 'name']},
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in', models.DateTimeField()),
                ('clock_out', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='attendance.employee')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='attendance.shift')),
            ],
            options={'ordering': ['-clock_in']},
        ),
    ]
