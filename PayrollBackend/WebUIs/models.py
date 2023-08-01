import uuid
from django.db import models

class Allowance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    date_created = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    effective_date = models.DateField(null=True)
    is_recurring = models.BooleanField()
    is_taxable = models.BooleanField()
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    payroll_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'allowances'


class AppUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    email = models.EmailField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    deleted_by = models.UUIDField(null=True)
    description = models.TextField(null=True)
    password = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    role_id = models.UUIDField(null=True)
    salary_id = models.UUIDField(null=True)
    department_id = models.UUIDField(null=True)
    business_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'app_user'


class ContactInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=13, null=True)
    contact_information_id = models.UUIDField(null=True)
    email = models.EmailField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'contact_information'


class Deduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    is_recurring = models.BooleanField()
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    payroll_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'deductions'


class Department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=255, null=True)
    details = models.TextField(null=True)

    class Meta:
        db_table = 'department'


class Earning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    description = models.TextField(null=True)
    earning_date = models.DateField(null=True)
    paid = models.BooleanField()
    payslip_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'earnings'


class Payroll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_salary = models.FloatField()
    date_created = models.DateTimeField(null=True)
    end_date = models.DateField(null=True)
    payment_mode = models.CharField(max_length=255, null=True)
    payment_period = models.CharField(max_length=255, null=True)
    payment_rate = models.CharField(max_length=255, null=True)
    ref_no = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=255, null=True)
    uncompleted_payments = models.IntegerField()
    unpaid_payslips = models.IntegerField()
    employee_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'payroll'


class Payslip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allowances = models.CharField(max_length=255, null=True)
    basic_salary = models.FloatField()
    deductions = models.CharField(max_length=255, null=True)
    earnings = models.CharField(max_length=255, null=True)
    end_date = models.DateField(null=True)
    fully_paid = models.BooleanField()
    issue_date = models.DateField(null=True)
    net_salary = models.FloatField()
    paid_amount = models.FloatField()
    payment_mode = models.CharField(max_length=255, null=True)
    payslip_no = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=255, null=True)
    total_allowances = models.FloatField()
    total_deductions = models.FloatField()
    total_earnings = models.FloatField()
    payroll_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'payslip'


class Salary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_date = models.IntegerField()
    salary = models.FloatField()

    class Meta:
        db_table = 'salary'


class UserRoles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    default_value = models.BooleanField()
    description = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    permissions = models.TextField(null=True)
    created_by = models.UUIDField(null=True)
    modified_by = models.UUIDField(null=True)
    business_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'user_roles'


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.UUIDField(null=True)
    date_created = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=255, null=True)
    contact_id = models.UUIDField(null=True)

    class Meta:
        db_table = 'business'
