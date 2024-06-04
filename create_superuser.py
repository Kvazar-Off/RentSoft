# create_superuser.py

# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rsadmin.settings')
# django.setup()

# from rsapp.models import Employee, User

# employee = Employee.objects.create(surname='Заяц', name='Александр', middlename='Сергеевич', phone_number='79197772116')
# user = User.objects.create_superuser('aszayats', 'aszayats@mail.ru', 'p6ketyup.', employee=employee)

# employee = Employee.objects.create(
#     surname='Заяц',
#     name='Александр',
#     middlename='Сергеевич',
#     phone_number='79197772116'
# )

# user = User.objects.create_superuser(
#     username='aszayats',
#     email='aszayats@mail.ru',
#     password='p6ketyup.',
#     employee=employee
# )

# employee = Employee.objects.create(
#     surname='Трифонов',
#     name='Сергей',
#     middlename='Алексеевич',
#     phone_number='79178956374'
# )

# user = User.objects.create_superuser(
#     username='satrifonov',
#     email='tsa@mail.ru',
#     password='U$atui228_',
#     employee=employee
# )