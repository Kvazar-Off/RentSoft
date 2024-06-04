from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator



# СОТРУДНИК
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='userphotos/%Y-%m-%d/', default='images/photo_not_found.jpg', null=True, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.middlename} {self.phone_number}'

    def get_photo_filename(self):
        return f'userphotos/{self.photo}' if self.photo else 'images/photo_not_found.jpg'

    def full_name(self):
        return f"{self.surname} {self.name} {self.middlename}"
    
    def fio(self):
        return f"{self.surname} {self.name[0]}.{self.middlename[0:1]}"
       

# ПОЛЬЗОВАТЕЛЬ
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.employee.full_name()}'


# ЗДАНИЕ
class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Название здания')
    address = models.CharField(max_length=200, verbose_name='Адрес здания')
    total_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Общая площадь помещений')
    total_rooms = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Общее количество помещений')

    def __str__(self):
        return (f'{self.name} {self.address}')


# АРЕНДНОЕ ПОМЕЩЕНИЕ
class RentalSpace(models.Model):
    rental_space_id = models.AutoField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Площадь помещения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание помещения')
    floor = models.IntegerField(verbose_name='Этаж')
    number = models.CharField(max_length=10, verbose_name='Номер помещения')
    curator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curated_spaces', verbose_name='Куратор помещения')
    status = models.ForeignKey('SpaceStatus', on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, related_name='rented_spaces', blank=True, null=True,)

    def __str__(self):
        return (f'{self.rental_space_id} {self.building} {self.area} {self.floor} {self.number} '
                f'{self.curator} {self.status} {self.tenant}')


# СТАТУС ПОМЕЩЕНИЯ
class SpaceStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, verbose_name='Статус помещения')

    def __str__(self):
        return self.description


# АРЕНДАТОР
class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100, verbose_name='Фамилия арендатора')
    name = models.CharField(max_length=100, verbose_name='Имя арендатора')
    middlename = models.CharField(max_length=100,null=True, verbose_name='Отчество арендатора')
    email = models.EmailField(unique=True, verbose_name='Почта арендатора')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона арендатора')
    organization_name = models.CharField(max_length=200, verbose_name='Наименование организации')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН организации')
    inn = models.CharField(max_length=12, verbose_name='ИНН организации')
    passport_series = models.CharField(max_length=4, verbose_name='Серия паспорта арендатора')
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта арендатора')
    bank_bik = models.CharField(max_length=9, verbose_name='БИК банка')
    bank_account = models.CharField(max_length=20, verbose_name='Расчетный счёт банка')
    total_payments = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True, verbose_name='Общая сумма выплат')
    rental_debt = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Текущая задолженность по арендным платежам')
    maintenance_debt = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Текущая задолженность по обслуживанию помещений')

    def __str__(self):
        return (f'{self.surname} {self.name} {self.middlename} {self.email} '
                f'{self.phone_number} {self.organization_name} {self.ogrn} {self.inn} {self.bank_bik} '
                f'{self.total_payments} {self.rental_debt} {self.maintenance_debt}')


# СЧЁТ ЗА ОБСЛУЖИВАНИЕ ПОМЕЩЕНИЯ
class MaintenanceBill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    rental_space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    gas_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Счет за газ')
    electricity_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Счет за электричество')
    water_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Счет за воду')
    heating_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Счет за отопление')
    repair_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Счет за ремонтные работы')
    creation_date = models.DateField(verbose_name='Дата создания счёта')

    def __str__(self):
        return (f'{self.rental_space} {self.gas_bill} {self.electricity_bill} {self.water_bill} '
                f'{self.heating_bill} {self.repair_bill} {self.creation_date}')



# АРЕНДНОЕ СОГЛАШЕНИЕ
class RentalAgreement(models.Model):
    agreement_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    rental_space = models.ForeignKey(RentalSpace, on_delete=models.CASCADE)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма ежемесячных выплат')
    start_date = models.DateField(verbose_name='Дата заключения соглашения')
    end_date = models.DateField(verbose_name='Дата завершения соглашения')
    payment_date = models.DateField(verbose_name='Дата списания ежемесячного арендного платежа')

    def __str__(self):
        return (f'{self.tenant} {self.tenant.surname} {self.tenant.name} {self.tenant.middlename}'
                f'{self.rental_space.number} {self.monthly_payment} {self.start_date} {self.end_date} {self.payment_date}')

# ДОГОВОР
class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    rental_agreement = models.OneToOneField(RentalAgreement, on_delete=models.CASCADE)
    signing_date = models.DateField(verbose_name='Дата подписания договора')
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True, verbose_name='Копия договора')
    status = models.CharField(max_length=50, verbose_name='Статус договора')

    def __str__(self):
        return f'{self.contract_id} {self.signing_date} {self.contract_file} {self.status})'



# ПЛАТЕЖ
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма платежа')
    payment_date = models.DateField(verbose_name='Дата платежа')
    payment_file = models.FileField(upload_to='payments/', blank=True, null=True, verbose_name='Копия платежа')
    category = models.ForeignKey('PaymentCategory', on_delete=models.CASCADE, verbose_name='Категория договора')

    def __str__(self):
        return f'{self.payment_id} {self.payment_date}{self.amount} {self.category.category_name})'


# КАТЕГОРИЯ ПЛАТЕЖА
class PaymentCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, verbose_name='Название категории платежа')

    def __str__(self):
        return f'{self.category_name}'

