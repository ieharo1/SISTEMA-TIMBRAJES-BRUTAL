from django import forms
from django.contrib.auth.models import User

from .models import AttendanceRecord, Employee


class BootstrapFormMixin:
    def _apply_bootstrap(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = (field.widget.attrs.get('class', '') + ' form-control').strip()


class ClockInForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    class Meta:
        model = AttendanceRecord
        fields = ['shift', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 2})}


class ClockOutForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    class Meta:
        model = AttendanceRecord
        fields = ['notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 2})}


class EmployeeForm(BootstrapFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=150)

    class Meta:
        model = Employee
        fields = ['employee_code', 'office', 'position', 'hourly_rate', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    def save(self, commit=True):
        employee = super().save(commit=False)
        user, _ = User.objects.get_or_create(username=self.cleaned_data['username'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        employee.user = user
        if commit:
            employee.save()
        return employee
