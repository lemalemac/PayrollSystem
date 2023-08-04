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

from .models import User, Deduction, Campus, Bonus, Commission, UserRoles, Payslip
from django.shortcuts import get_object_or_404
import weasyprint

def app(request):
    if request.session.get('login_flag'):
        return render(request, "app.html", {})
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


def generate_pdf(request):
    if request.method == "POST":
        document_type = request.POST.get('first_name')
        # Render the HTML template using Django's render function
        html_template = 'templates/forms/bootstrap_template.html'
        rendered_html = render(request, html_template).content

        # Generate PDF from the rendered HTML
        pdf_file = weasyprint.HTML(string=rendered_html).write_pdf()

        # Create an HttpResponse with the PDF content and appropriate headers
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="your_bootstrap_page.pdf"'
        return response
