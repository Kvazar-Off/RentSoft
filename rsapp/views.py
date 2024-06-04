import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from rsapp.forms import *
from django.shortcuts import render
from django.utils import timezone
import pandas as pd
import matplotlib.pyplot as plt
import base64
import matplotlib.pyplot as plt
import io
from PIL import Image


from django.shortcuts import render
from .models import RentalSpace, Payment
from django.db.models import Count, Sum
import pandas as pd

@login_required
def payments(request):
    return render(request, 'payments.html', {'title': 'RentSoft | Оплата'})


def auth(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        u_login = request.POST['authloginame']
        password = request.POST['authpasswordname']

        user = authenticate(request, username=u_login, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('account'))

    return render(request, 'auth.html', {'title': 'RentSoft | Авторизация'})

@login_required
def account(request):
    user_info = request.user
    employee_info = user_info.employee

    if request.method == 'POST':
        user_photo_uploaded = request.FILES['user_photo_upload']
        allowed_extensions = ['.jpg', '.png']
        ext = os.path.splitext(user_photo_uploaded.name)[1]

        if ext.lower() not in allowed_extensions:
            raise ValidationError('Only JPG, and PNG files are allowed.')
        else:
            employee_info.photo = user_photo_uploaded
            employee_info.save()

    return render(request, 'account.html', {'user_info': user_info, 'employee_info': employee_info, 'title': 'RentSoft | Профиль'})



@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()
    
    if request.method == 'GET':
        filter_form = TenantFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data['tenant_id']:
                tenants = tenants.filter(tenant_id=filter_form.cleaned_data['tenant_id'])
            if filter_form.cleaned_data['organization_name']:
                tenants = tenants.filter(organization_name__icontains=filter_form.cleaned_data['organization_name'])
            if filter_form.cleaned_data['surname']:
                tenants = tenants.filter(surname__icontains=filter_form.cleaned_data['surname'])
            if filter_form.cleaned_data['name']:
                tenants = tenants.filter(name__icontains=filter_form.cleaned_data['name'])
            if filter_form.cleaned_data['phone_number']:
                tenants = tenants.filter(phone_number__icontains=filter_form.cleaned_data['phone_number'])
            if filter_form.cleaned_data['manager']:
                tenants = tenants.filter(rented_spaces__curator=filter_form.cleaned_data['manager'])
            if filter_form.cleaned_data['rental_debt']:
                tenants = tenants.filter(rental_debt__gte=filter_form.cleaned_data['rental_debt'])
            if filter_form.cleaned_data['maintenance_debt']:
                tenants = tenants.filter(maintenance_debt__gte=filter_form.cleaned_data['maintenance_debt'])
    else:
        filter_form = TenantFilterForm()

    return render(request, 'tenant_list.html', {'tenants': tenants, 'filter_form': filter_form})


@login_required
def tenant_add(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'tenant_form.html', {'form': form})

@login_required
def create_agreement(request):
    if request.method == 'POST':
        form = RentalAgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contracts')  # Замените на ваш список договоров
    else:
        form = RentalAgreementForm()
    return render(request, 'create_agreement.html', {'form': form})


@login_required
def add_tenant_modal(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save()
            return redirect(f'{reverse("create_agreement")}?tenant_id={tenant.tenant_id}')
    else:
        form = TenantForm()
    
    return render(request, 'tenant_form_modal.html', {'form': form, 'is_modal': True})


@login_required
def tenant_edit(request, tenant_id):
    tenant = get_object_or_404(Tenant, tenant_id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'tenant_form.html', {'form': form})

@login_required
def tenant_delete(request, tenant_id):
    tenant = get_object_or_404(Tenant, tenant_id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'tenant_confirm_delete.html', {'tenant': tenant})


#  Работа с помещениями
# --------------------------------
def rental_objects(request):
    rental_spaces = RentalSpace.objects.all()
    building_filter = request.GET.get('building')
    floor_filter = request.GET.get('floor')
    number_filter = request.GET.get('number')
    status_filter = request.GET.get('status')
    area_filter = request.GET.get('area')
    tenant_filter = request.GET.get('tenant')
    curator_filter = request.GET.get('curator')

    if building_filter:
        rental_spaces = rental_spaces.filter(building__name__icontains=building_filter)
    if floor_filter:
        rental_spaces = rental_spaces.filter(floor=floor_filter)
    if number_filter:
        rental_spaces = rental_spaces.filter(number__icontains=number_filter)
    if status_filter:
        try:
            status = SpaceStatus.objects.get(description=status_filter)
            rental_spaces = rental_spaces.filter(status=status.status_id)
        except SpaceStatus.DoesNotExist:
            rental_spaces = rental_spaces.none()
    if area_filter:
        rental_spaces = rental_spaces.filter(area=area_filter)
    if tenant_filter:
        rental_spaces = rental_spaces.filter(tenant__surname__icontains=tenant_filter)
    if curator_filter:
        rental_spaces = rental_spaces.filter(
            models.Q(curator__employee__surname__icontains=curator_filter) |
            models.Q(curator__employee__name__icontains=curator_filter) |
            models.Q(curator__employee__middlename__icontains=curator_filter)
        )

    return render(request, 'rental_objects.html', {'rental_spaces': rental_spaces})

@login_required
def add_rental_space(request):
    if request.method == 'POST':
        form = RentalSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental_objects')
    else:
        form = RentalSpaceForm()
    return render(request, 'add_rental_space.html', {'form': form})

@login_required
def edit_rental_space(request, pk):
    rental_space = get_object_or_404(RentalSpace, pk=pk)
    if request.method == 'POST':
        form = RentalSpaceForm(request.POST, instance=rental_space)
        if form.is_valid():
            form.save()
            return redirect('rental_objects')
    else:
        form = RentalSpaceForm(instance=rental_space)
    return render(request, 'edit_rental_space.html', {'form': form})


@login_required
def delete_rental_space(request, pk):
    rental_space = get_object_or_404(RentalSpace, pk=pk)
    if request.method == 'POST':
        rental_space.delete()
        return redirect('rental_objects')
    return render(request, 'delete_rental_space.html', {'rental_space': rental_space})
# --------------------------------

@login_required
def contracts(request):
    agreements = RentalAgreement.objects.all()

    # Фильтрация данных по GET-параметрам
    doc_num_filter = request.GET.get('agreement_id')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    paid_until_filter = request.GET.get('paid_until')
    organization_name_filter = request.GET.get('organization_name')

    if doc_num_filter:
        agreements = agreements.filter(agreement_id=doc_num_filter)
    if start_date_filter:
        agreements = agreements.filter(start_date__gte=start_date_filter)
    if end_date_filter:
        agreements = agreements.filter(end_date__lte=end_date_filter)
    if paid_until_filter:
        paid_until_date = timezone.datetime.strptime(paid_until_filter, '%Y-%m-%d').date()
        agreements = agreements.filter(payment_date__lte=paid_until_date)
    if organization_name_filter:
        agreements = agreements.filter(tenant__organization_name__icontains=organization_name_filter)

    # Дополнительные поля
    for agreement in agreements:
        latest_payment = Payment.objects.filter(rental_agreement=agreement).order_by('-payment_date').first()
        agreement.paid_until = latest_payment.payment_date + timezone.timedelta(days=30) if latest_payment else None
        agreement.is_active = "да" if agreement.end_date >= timezone.now().date() else "нет"

    return render(request, 'contracts.html', {'agreements': agreements})


def delete_contract(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    
    if request.method == 'POST':
        contract.delete()
        return redirect('contracts') 
    context = {
        'contract': contract
    }
    return render(request, 'delete_contract.html', context)


@login_required
def settings(request):
    return render(request,'settings.html', {'title': 'RentSoft | Настройки'})


@login_required
# Список зданий
def buildings(request):
    buildings = Building.objects.all()
    return render(request, 'buildings.html', {'buildings': buildings})

# Добавление здания
@login_required
def add_building(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        total_area = request.POST['total_area']
        total_rooms = request.POST['total_rooms']

        Building.objects.create(
            name=name,
            address=address,
            total_area=total_area,
            total_rooms=total_rooms
        )
        return redirect('buildings')
    
    return render(request, 'add_building.html')

# Изменение здания
@login_required
def edit_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.method == 'POST':
        building.name = request.POST['name']
        building.address = request.POST['address']
        building.total_area = request.POST['total_area']
        building.total_rooms = request.POST['total_rooms']
        building.save()
        return redirect('buildings')
    
    return render(request, 'edit_building.html', {'building': building})

# Удаление здания
@login_required
def delete_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.method == 'POST':
        building.delete()
        return redirect('buildings')
    
    return render(request, 'delete_building.html', {'building': building})

# Менеджеры
@login_required
def managers(request):
    managers = User.objects.all()
    return render(request, 'managers.html', {'managers': managers})


@login_required
def add_manager(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES)
        user_form = CustomUserCreationForm(request.POST)

        if employee_form.is_valid() and user_form.is_valid():
            employee = employee_form.save()
            user = user_form.save(commit=False)
            user.employee = employee
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            return redirect('managers')

    else:
        employee_form = EmployeeForm()
        user_form = CustomUserCreationForm()

    return render(request, 'add_manager.html', {'employee_form': employee_form, 'user_form': user_form})


@login_required
def edit_manager(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = get_object_or_404(User, employee=employee)
    
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        user_form = CustomUserChangeForm(request.POST, instance=user)
        
        if employee_form.is_valid() and user_form.is_valid():
            employee_form.save()
            user_form.save()
            return redirect('managers')

    else:
        employee_form = EmployeeForm(instance=employee)
        user_form = CustomUserChangeForm(instance=user)
    
    return render(request, 'edit_manager.html', {
        'employee_form': employee_form,
        'user_form': user_form,
    })

@login_required
def delete_manager(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user

    if request.method == 'POST':
        employee.delete()
        user.delete()
        return redirect('managers')

    return render(request, 'delete_confirmation.html', {'employee': employee, 'user': user})


@login_required
def bills_view(request):
    bills = MaintenanceBill.objects.all()

    rental_space_filter = request.GET.get('rental_space')
    creation_date_filter = request.GET.get('creation_date')

    if rental_space_filter:
        bills = bills.filter(rental_space__number__icontains=rental_space_filter)
    if creation_date_filter:
        bills = bills.filter(creation_date__gte=creation_date_filter)


    context = {
        'bills': bills,
    }
    return render(request, 'bills.html', context)

@login_required
def add_bill_view(request):
    if request.method == "POST":
        form = MaintenanceBillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bills')
    else:
        form = MaintenanceBillForm()
    return render(request, 'bill_form.html', {'form': form})

@login_required
def edit_bill_view(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, pk=bill_id)
    if request.method == "POST":
        form = MaintenanceBillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bills')
    else:
        form = MaintenanceBillForm(instance=bill)
    return render(request, 'bill_form.html', {'form': form})

@login_required
def delete_bill_view(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, pk=bill_id)
    if request.method == "POST":
        bill.delete()
        return redirect('bills')
    return render(request, 'bill_confirm_delete.html', {'bill': bill})


@login_required
def payments(request):
    payments = Payment.objects.all()

    # Фильтрация данных по GET-параметрам
    rental_space_filter = request.GET.get('rental_space')
    tenant_filter = request.GET.get('organization_name')
    payment_date_filter = request.GET.get('payment_date')

    if rental_space_filter:
        payments = payments.filter(rental_agreement__rental_space__icontains=rental_space_filter)
    if tenant_filter:
        payments = payments.filter(rental_agreement__tenant__organization_name__icontains=tenant_filter)
    if payment_date_filter:
        payments = payments.filter(payment_date=payment_date_filter)

    return render(request, 'payments.html', {'payments': payments})

@login_required
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payments')  # Перенаправляем пользователя на страницу с платежами после создания платежа
    else:
        form = PaymentForm()
    return render(request, 'create_payment.html', {'form': form})

@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payments')  # Перенаправляем пользователя на страницу с платежами после редактирования платежа
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form})

def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    if request.method == 'POST':
        payment.delete()
        return redirect('payments')  # Перенаправляем пользователя на страницу с платежами после удаления платежа
    return render(request, 'delete_payment.html', {'payment': payment})

@login_required
def analytics_view(request):
    return render(request, 'analytics.html')

def analytics(request):
    # Подготовка данных для круговой диаграммы состояний объектов недвижимости
    status_counts = RentalSpace.objects.values('status__description').annotate(count=Count('status'))
    pie_labels = [item['status__description'] for item in status_counts]
    pie_sizes = [item['count'] for item in status_counts]

    # Подготовка данных для гистограммы поступлений платежей по месяцам
    payments = Payment.objects.all().values('payment_date', 'amount')
    df = pd.DataFrame(payments)
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    df = df.set_index('payment_date')
    monthly_sums = df.resample('M').sum().reset_index()
    bar_labels = monthly_sums['payment_date'].dt.strftime('%Y-%m').tolist()
    bar_data = monthly_sums['amount'].tolist()

    # Подготовка данных для диаграммы состояний объектов недвижимости по статусу
    rental_spaces = RentalSpace.objects.select_related('status').all()
    timeline_data = []
    for space in rental_spaces:
        timeline_data.append({
            'label': f'{space.floor}-{space.number}',
            'status': space.status.description,
            'start_date': space.rentalagreement_set.first().start_date.strftime('%Y-%m-%d') if space.rentalagreement_set.exists() else None,
            'end_date': space.rentalagreement_set.first().end_date.strftime('%Y-%m-%d') if space.rentalagreement_set.exists() else None
        })

    context = {
        'pie_labels': pie_labels,
        'pie_sizes': pie_sizes,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'timeline_data': timeline_data
    }
    return render(request, 'analytics.html', context)






@login_required
def logout_(request):
    logout(request)
    return redirect('auth')
