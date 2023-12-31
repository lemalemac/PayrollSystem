from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import uuid
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.core.serializers import serialize

from .models import User, Deduction, Campus, Bonus, Commission, UserRoles, Payslip, Salary
from django.shortcuts import get_object_or_404
import pandas as pd
from django.utils import timezone
from django.db.models import Sum
from django.db import models


def app(request):
    if request.session.get('login_flag'):
        # Count the total number of users
        total_users = User.objects.count()

        # Calculate total paye, nssf, nhif, and total basic salary
        total_paye = Deduction.objects.filter(name='paye').aggregate(total_paye=models.Sum('amount'))['total_paye'] or 0
        total_nssf = Deduction.objects.filter(name='nssf').aggregate(total_nssf=models.Sum('amount'))['total_nssf'] or 0
        total_nhif = Deduction.objects.filter(name='nhif').aggregate(total_nhif=models.Sum('amount'))['total_nhif'] or 0
        total_basic_salary = User.objects.aggregate(total_basic_salary=models.Sum('basic_salary'))[
                                 'total_basic_salary'] or 0

        context = {
            'total_users': total_users,
            'total_paye': total_paye,
            'total_nssf': total_nssf,
            'total_nhif': total_nhif,
            'total_basic_salary': total_basic_salary
        }

        return render(request, "app.html", context)
    return render(request, "home.html", {})


def login_user(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        password = request.POST['password']

        user = authenticate(request, employee_id=employee_id, password=password)
        if user is not None:
            print("success")
            login(request, user)
            request.session['login_flag'] = True
            data = {
                'message': 'success'
            }
            return JsonResponse(data)
        else:
            print("error")
            data = {
                'message': 'auth_error'
            }
            return JsonResponse(data)

    return render(request, "login.html", {})


def create_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        title = request.POST.get('title')
        campus_id = request.POST.get('campus')
        school = request.POST.get('school')
        department = request.POST.get('department')
        role_id = request.POST.get('role')
        basic_salary = request.POST.get('basic_salary')
        payment_method = request.POST.get('payment_method')
        payment_details = request.POST.get('payment_details')
        paye = request.POST.get('paye')
        nssf = request.POST.get('nssf')
        nhif = request.POST.get('nhif')
        helb = request.POST.get('helb')
        id_no = request.POST.get('id_no')
        kra_pin = request.POST.get('kra_pin')
        nssf_no = request.POST.get('nssf_no')
        nhif_no = request.POST.get('nhif_no')
        password = request.POST.get('password')

        if helb is None:
            helb = 0

        # Handle all IDs and their appropriate models here
        random_number = random.randint(1000, 9999)
        employee_id = f"jkuat-{random_number}"
        salary_id = str(uuid.uuid4())
        str(uuid.uuid4())

        # Create the new user instance
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            title=title,
            campus_id=campus_id,
            school=school,
            department=department,
            role_id=role_id,
            basic_salary=basic_salary,
            payment_method=payment_method,
            payment_details=payment_details,
            employee_id=employee_id,
            salary_id=salary_id,
            password=password,
            id_no=id_no,
            kra_pin=kra_pin,
            nssf_no=nssf_no,
            nhif_no=nhif_no
        )

        # Create Deduction instances and associate them with the new_user
        Deduction.objects.create(id=str(uuid.uuid4()), amount=float(paye), is_recurring=True, name='paye', user=new_user)
        Deduction.objects.create(id=str(uuid.uuid4()), amount=float(helb), is_recurring=False, name='helb', user=new_user)
        Deduction.objects.create(id=str(uuid.uuid4()), amount=float(nssf), is_recurring=True, name='nssf', user=new_user)
        Deduction.objects.create(id=str(uuid.uuid4()), amount=float(nhif), is_recurring=False, name='nhif', user=new_user)

        user = authenticate(request, employee_id=employee_id, password=password)
        if user is not None:
            login(request, user)
            request.session['login_flag'] = True
            print("success")
        else:
            print("error")

        data = {
            'message': 'success'
        }
        return JsonResponse(data)



        '''# Create Bonus instances and associate them with the new_user
        bonus_instance = Bonus.objects.create(amount=200, is_recurring=True, name='Bonus 1', user=new_user)

        # Create Commission instances and associate them with the new_user
        commission_instance = Commission.objects.create(amount=300, is_recurring=True, name='Commission 1', user=new_user)

        # Create Payslip instance and associate it with the new_user and related deductions, bonuses, and commissions
        payslip = Payslip.objects.create(
            basic_salary=2000,
            net_salary=1800,
            paid_amount=1800,
            fully_paid=True,
            user=new_user
        )
        payslip.deductions.add(PAYE, HELB, NSSF, NHIF)
        payslip.bonuses.add(bonus)
        payslip.commissions.add(commission)'''

    return render(request, "create.html", {})


def search(request):
    if request.method == "POST":
        try:
            employee_id = request.POST.get('employee_id')

            user = User.objects.get(employee_id=employee_id)

            # Customize the JSON response here
            custom_response = {
                'message': 'success',
                'employee_id': user.employee_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone
            }

            print(custom_response)
            return JsonResponse(custom_response)
        except User.DoesNotExist:
            data = {
                'message': 'error'
            }
            return JsonResponse(data)


def employee_details_view(request, employee_id):
    try:
        user = User.objects.get(employee_id=employee_id)
        context = {
            'user': user,
            'message': 'success',
            'employee_id': user.employee_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'school': user.school,
            'title': user.title,
            'department': user.department,
            'payment_method': user.payment_method,
            'payment_details': user.payment_details,
            'basic_salary': user.basic_salary,
            'id_no': user.id_no,
            'kra_pin': user.kra_pin,
            'nhif_no': user.nhif_no,
            'nssf_no': user.nssf_no

        }
        print(context)
        return render(request, 'search_view.html', context)
    except User.DoesNotExist:
        return redirect("app")


def modify(request):
    user = str(request.user)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        title = request.POST.get('title')
        campus_id = request.POST.get('campus')
        school = request.POST.get('school')
        department = request.POST.get('department')
        role_id = request.POST.get('role')
        basic_salary = request.POST.get('basic_salary')
        payment_method = request.POST.get('payment_method')
        payment_details = request.POST.get('payment_details')
        id_no = request.POST.get('id_no')
        kra_pin = request.POST.get('kra_pin')
        nssf_no = request.POST.get('nssf_no')
        nhif_no = request.POST.get('nhif_no')

        user = get_object_or_404(User, employee_id=user)

        # Update the user instance with the new values
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.title = title
        user.campus_id = campus_id
        user.school = school
        user.department = department
        user.role_id = role_id
        user.basic_salary = basic_salary
        user.payment_method = payment_method
        user.payment_details = payment_details
        user.id_no = id_no
        user.kra_pin = kra_pin
        user.nssf_no = nssf_no
        user.nhif_no = nhif_no

        user.save()

        data = {
            'message': 'success'
        }
        return JsonResponse(data)


def delete(request):
    user = str(request.user)
    user = get_object_or_404(User, employee_id=user)

    # Delete the user instance
    user.delete()

    data = {
        'message': 'success'
    }
    return JsonResponse(data)


def audit_export_to_excel(request):
    # Fetch data from the YourModel model
    queryset = Salary.objects.all()
    data = list(queryset.values())

    # Convert to a pandas DataFrame
    dataframe = pd.DataFrame(data)

    # Prepare the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=output.xlsx'
    response['Cache-Control'] = 'no-cache'

    # Export the DataFrame to Excel and attach it to the response
    dataframe.to_excel(response, index=False, engine='openpyxl')

    return response


def kra_export_to_excel(request):
    # Fetch data for "paye" deductions from the Deduction model
    paye_deductions = Deduction.objects.filter(name="paye")

    # Collect the associated User data for each "paye" deduction
    data = []
    for deduction in paye_deductions:
        user_data = {
            'user_name': deduction.user.first_name + ' ' + deduction.user.last_name,
            'kra_pin': deduction.user.kra_pin,
            'basic_salary': deduction.user.basic_salary,
            'deduction_amount': deduction.amount,
            'is_recurring': deduction.is_recurring,
            'deduction_date_added': deduction.date_added.astimezone(timezone.utc).replace(tzinfo=None)

        }
        data.append(user_data)

    # Convert to a pandas DataFrame
    dataframe = pd.DataFrame(data)

    # Prepare the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=KRA_P10.xlsx'
    response['Cache-Control'] = 'no-cache'

    # Export the DataFrame to Excel and attach it to the response
    dataframe.to_excel(response, index=False, engine='openpyxl')

    return response


def nssf_export_to_excel(request):

    nssf_deductions = Deduction.objects.filter(name="nssf")

    data = []
    for deduction in nssf_deductions:
        user_data = {
            'user_name': deduction.user.first_name + ' ' + deduction.user.last_name,
            'nssf_no': deduction.user.nssf_no,
            'basic_salary': deduction.user.basic_salary,
            'deduction_amount': deduction.amount,
            'is_recurring': deduction.is_recurring,
            'deduction_date_added': deduction.date_added.astimezone(timezone.utc).replace(tzinfo=None)

        }
        data.append(user_data)

    # Convert to a pandas DataFrame
    dataframe = pd.DataFrame(data)

    # Prepare the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=NSSF_BYPRODUCT.xlsx'
    response['Cache-Control'] = 'no-cache'

    # Export the DataFrame to Excel and attach it to the response
    dataframe.to_excel(response, index=False, engine='openpyxl')

    return response


def nhif_export_to_excel(request):

    nhif_deductions = Deduction.objects.filter(name="nhif")

    data = []
    for deduction in nhif_deductions:
        user_data = {
            'user_name': deduction.user.first_name + ' ' + deduction.user.last_name,
            'nhif_no': deduction.user.nhif_no,
            'basic_salary': deduction.user.basic_salary,
            'deduction_amount': deduction.amount,
            'is_recurring': deduction.is_recurring,
            'deduction_date_added': deduction.date_added.astimezone(timezone.utc).replace(tzinfo=None)

        }
        data.append(user_data)

    # Convert to a pandas DataFrame
    dataframe = pd.DataFrame(data)

    # Prepare the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=NHIF_BYPRODUCT.xlsx'
    response['Cache-Control'] = 'no-cache'

    # Export the DataFrame to Excel and attach it to the response
    dataframe.to_excel(response, index=False, engine='openpyxl')

    return response
