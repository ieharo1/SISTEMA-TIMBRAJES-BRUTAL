from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/<int:pk>/', views.clock_out, name='clock_out'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('reports/', views.reports, name='reports'),
    path('reports/export-csv/', views.export_report_csv, name='export_report_csv'),
]
