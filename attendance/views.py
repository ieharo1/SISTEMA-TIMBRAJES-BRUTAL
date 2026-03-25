import csv
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ClockInForm, ClockOutForm, EmployeeForm
from .models import AttendanceRecord, Employee


@login_required
def dashboard(request):
    employee = Employee.objects.filter(user=request.user).first()
    open_record = AttendanceRecord.objects.filter(employee=employee, clock_out__isnull=True).first() if employee else None
    recent_records = AttendanceRecord.objects.select_related('employee__user', 'shift', 'employee__office')[:10]

    total_worked = sum(r.worked_minutes for r in recent_records)
    total_overtime = sum(r.overtime_minutes for r in recent_records)

    context = {
        'employee': employee,
        'open_record': open_record,
        'recent_records': recent_records,
        'total_worked_hours': round(total_worked / 60, 2),
        'total_overtime_hours': round(total_overtime / 60, 2),
        'clock_in_form': ClockInForm(),
    }
    return render(request, 'attendance/dashboard.html', context)


@login_required
def clock_in(request):
    employee = get_object_or_404(Employee, user=request.user)
    if AttendanceRecord.objects.filter(employee=employee, clock_out__isnull=True).exists():
        messages.warning(request, 'Ya tienes un timbraje abierto.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ClockInForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.employee = employee
            record.clock_in = timezone.now()
            record.save()
            messages.success(request, 'Entrada registrada exitosamente.')
    return redirect('dashboard')


@login_required
def clock_out(request, pk):
    employee = get_object_or_404(Employee, user=request.user)
    record = get_object_or_404(AttendanceRecord, pk=pk, employee=employee)

    if request.method == 'POST':
        form = ClockOutForm(request.POST, instance=record)
        if form.is_valid():
            out_record = form.save(commit=False)
            out_record.clock_out = timezone.now()
            out_record.save()
            messages.success(request, 'Salida registrada correctamente.')

    return redirect('dashboard')


@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user', 'office')
    return render(request, 'attendance/employee_list.html', {'employees': employees})


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado con éxito.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'attendance/employee_form.html', {'form': form})


@login_required
def reports(request):
    records = AttendanceRecord.objects.select_related('employee__user', 'employee__office', 'shift')

    start = request.GET.get('start')
    end = request.GET.get('end')
    office = request.GET.get('office')

    if start:
        records = records.filter(clock_in__date__gte=start)
    if end:
        records = records.filter(clock_in__date__lte=end)
    if office:
        records = records.filter(employee__office__id=office)

    summary = {
        'worked_hours': round(sum(r.worked_minutes for r in records) / 60, 2),
        'overtime_hours': round(sum(r.overtime_minutes for r in records) / 60, 2),
        'regular_pay': round(sum(r.regular_pay for r in records), 2),
        'overtime_pay': round(sum(r.overtime_pay for r in records), 2),
    }

    offices = {r.employee.office for r in AttendanceRecord.objects.select_related('employee__office')}

    context = {
        'records': records[:300],
        'summary': summary,
        'offices': sorted(offices, key=lambda x: x.name),
        'filters': {'start': start, 'end': end, 'office': office},
    }
    return render(request, 'attendance/reports.html', context)


@login_required
def export_report_csv(request):
    records = AttendanceRecord.objects.select_related('employee__user', 'employee__office', 'shift')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_timbrajes.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Empleado', 'Codigo', 'Oficina', 'Fecha', 'Entrada', 'Salida',
        'Horas Trabajadas', 'Horas Extras', 'Pago Regular', 'Pago Extra'
    ])

    for r in records:
        writer.writerow([
            r.employee.user.get_full_name() or r.employee.user.username,
            r.employee.employee_code,
            r.employee.office.name,
            r.clock_in.date(),
            r.clock_in.strftime('%H:%M'),
            r.clock_out.strftime('%H:%M') if r.clock_out else 'Pendiente',
            r.worked_hours_decimal,
            r.overtime_hours_decimal,
            r.regular_pay,
            r.overtime_pay,
        ])

    return response
