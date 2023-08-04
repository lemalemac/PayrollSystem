import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser, Group, Permission
from django.utils import timezone
from datetime import timedelta


class UserRoles(models.Model):
    role_id = models.CharField(primary_key=True, editable=False, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True)
    permissions = models.TextField(null=True)

    class Meta:
        db_table = 'user_roles'


class Campus(models.Model):
    campus_id = models.CharField(primary_key=True, editable=False, max_length=255)
    campus_name = models.CharField(max_length=255, null=True)
    details = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'campus'


class Payroll(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255)
    base_salary = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    payment_mode = models.CharField(max_length=255, null=True)
    payment_period = models.CharField(max_length=255, null=True)
    ref_no = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    employee_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'payroll'


class UserManager(BaseUserManager):

    def _create_user(self, employee_id, password, is_staff, is_superuser, **extra_fields):
        if not employee_id:
            raise ValueError('Users must have an employee ID')
        now = timezone.now()
        user = self.model(
            employee_id=employee_id,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, employee_id, password, **extra_fields):
        return self._create_user(employee_id, password, False, False, **extra_fields)

    def create_superuser(self, employee_id, password, **extra_fields):
        user = self._create_user(employee_id, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    employee_id = models.CharField(primary_key=True, editable=False, max_length=255)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    deleted_by = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    role_id = models.CharField(max_length=255, null=True)
    salary_id = models.CharField(max_length=255, null=True)
    campus_id = models.CharField(max_length=255, null=True)
    school = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    payment_method = models.CharField(max_length=255, null=True)
    payment_details = models.CharField(max_length=255, null=True)
    basic_salary = models.FloatField(default=0)
    id_no = models.FloatField(null=True)
    kra_pin = models.CharField(max_length=255, null=True)
    nssf_no = models.CharField(max_length=255, null=True)
    nhif_no = models.CharField(max_length=255, null=True)


    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'employee_id'
    EMPLOYEE_ID_FIELD = 'employee_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % self.pk

    # Define the ManyToManyField with a unique related_name for 'groups'
    groups = models.ManyToManyField(Group, related_name='web_users')

    # Define the ManyToManyField with a unique related_name for 'user_permissions'
    user_permissions = models.ManyToManyField(Permission, related_name='web_users')


class Deduction(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255)
    amount = models.FloatField()
    is_recurring = models.BooleanField()
    name = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'deductions'

    # Add ForeignKey field to establish the relationship between User and Deduction
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deductions', null=True)


class Bonus(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255)
    amount = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    effective_date = models.DateField(null=True)
    is_recurring = models.BooleanField()
    is_taxable = models.BooleanField()
    name = models.CharField(max_length=255, null=True)
    payroll_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'bonuses'

    # Add ForeignKey field to establish the relationship between User and Bonus
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonus', null=True)


class Commission(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255)
    amount = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    effective_date = models.DateField(null=True)
    is_recurring = models.BooleanField()
    is_taxable = models.BooleanField()
    name = models.CharField(max_length=255, null=True)
    payroll_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'commissions'

    # Add ForeignKey field to establish the relationship between User and Commission
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission', null=True)


class Payslip(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=255)
    basic_salary = models.FloatField()
    deductions = models.ManyToManyField(Deduction)
    bonuses = models.ManyToManyField(Bonus)
    commissions = models.ManyToManyField(Commission)
    earnings = models.CharField(max_length=255, null=True)
    end_date = models.DateField(null=True)
    fully_paid = models.BooleanField()
    issue_date = models.DateField(null=True)
    net_salary = models.FloatField()
    paid_amount = models.FloatField()
    payment_mode = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=255, null=True)

    # Add ForeignKey field to establish the relationship between User and Payslip
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payslips', null=True)


class Salary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_date = models.IntegerField()
    salary = models.FloatField()

    class Meta:
        db_table = 'salary'