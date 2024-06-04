from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'total_area', 'total_rooms')

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('surname', 'name', 'middlename', 'phone_number', 'photo')
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'middlename': 'Отчество',
            'phone_number': 'Номер телефона',
            'photo': 'Фотография',
        }
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),        }

class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        required=False,
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.username

class RentalSpaceForm(forms.ModelForm):
    class Meta:
        model = RentalSpace
        fields = ['building', 'floor', 'number', 'status', 'area', 'tenant', 'curator', 'description']
        labels = {
            'building': 'Здание',
            'floor': 'Этаж',
            'number': 'Номер помещения',
            'status': 'Статус',
            'area': 'Площадь',
            'tenant': 'Арендатор',
            'curator': 'Менеджер',
            'description': 'Комментарий',
        }
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'curator': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tenant'].required = False  # Сделать поле tenant необязательным


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'surname',
            'name',
            'middlename',
            'phone_number',
            'email',
            'organization_name',
            'ogrn',
            'inn',
            'passport_series',
            'passport_number',
            'bank_bik',
            'bank_account',
        ]
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'middlename': 'Отчество',
            'phone_number': 'Номер телефона',
            'email': 'Электронная почта',
            'organization_name': 'Название организации',
            'ogrn': 'ОГРН',
            'inn': 'ИНН',
            'passport_series': 'Серия паспорта',
            'passport_number': 'Номер паспорта',
            'bank_bik': 'БИК банка',
            'bank_account': 'Расчетный счет',
        }
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_series': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_bik': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TenantFilterForm(forms.Form):
    tenant_id = forms.CharField(max_length=10, required=False, label='ID')
    organization_name = forms.CharField(max_length=200, required=False, label='Компания')
    surname = forms.CharField(max_length=100, required=False, label='Фамилия')
    name = forms.CharField(max_length=100, required=False, label='Имя')
    phone_number = forms.CharField(max_length=20, required=False, label='Телефон')
    manager = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Менеджер')
    rental_debt = forms.DecimalField(max_digits=15, decimal_places=2, required=False, label='Задолженность по арендным платежам')
    maintenance_debt = forms.DecimalField(max_digits=15, decimal_places=2, required=False, label='Задолженность по обслуживанию помещений')


class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = [
            'tenant', 'rental_space', 'start_date', 'end_date',
            'monthly_payment', 'payment_date'
        ]
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-select'}),
            'rental_space': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MaintenanceBillForm(forms.ModelForm):
    class Meta:
        model = MaintenanceBill
        fields = [
            'rental_space', 
            'electricity_bill', 
            'gas_bill', 
            'water_bill', 
            'heating_bill', 
            'repair_bill', 
            'creation_date'
        ]
        widgets = {
            'rental_space': forms.Select(attrs={'class': 'form-select'}),
            'electricity_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'gas_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'water_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'heating_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'repair_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'rental_agreement', 
            'amount', 
            'payment_date', 
            'payment_file', 
            'category'
        ]
        widgets = {
            'rental_agreement': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_file': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }