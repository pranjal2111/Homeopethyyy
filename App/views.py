import random
import string

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage, message
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from .models import *

# Create your views here.

def index(request):
    fetchservice=Service.objects.all()[:3]
    fetchdoctor = Doctor.objects.all()[:3]
    context = {
        "data": fetchservice,
        "ddata":fetchdoctor
    }

    return render(request,"index.html",context)

def signup(request):
    return render(request,"sign-up.html")

def signupdata(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone_number = request.POST.get("phone_number")
    password = request.POST.get("password")
    user_dp = request.FILES["user_dp"]
    city = request.POST.get("city")
    state= request.POST.get("state")

    if User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
        messages.error(request, "Account already exists, please sign-in now.")
        return render(request, "sign-in.html")

    else:
        User.objects.all()

    insertquery = User(name=name, email=email, phone_number=phone_number, password=password,user_dp=user_dp,city=city,state=state)
    insertquery.save()
    messages.success(request, "Registered Successfully!")

    return render(request,"sign-in.html")

def signin(request):
    return render(request,"sign-in.html")

def signindata(request):
    identifier = request.POST.get("name")
    password = request.POST.get("password")

    try:

        if '@' in identifier:
            userdata = User.objects.get(email=identifier, password=password)
        else:
            userdata = User.objects.get(phone_number=identifier, password=password)
        print(userdata)

        request.session["log_id"] = userdata.id
        request.session["log_name"] = userdata.name
        request.session["log_email"] = userdata.email
        request.session["log_dp"] = userdata.user_dp.url

        print("session name:", request.session["log_name"])
        messages.success(request, "Login Successfully!")

        return redirect("/")

    except:
        messages.error(request, "Invalid Credentials!!")
        return render(request, "sign-in.html")

def signout(request):
    try:
        del request.session["log_id"]
        del request.session["log_name"]
        del request.session["log_email"]
        del request.session["log_dp"]
    except:
        pass
    return redirect("/sign-in")

def contact(request):
    return render(request,"contact.html")

def contactdata(request):
    user_id = request.session["log_id"]
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone_number = request.POST.get("phone_number")
    msg_subject = request.POST.get("msg_subject")
    message = request.POST.get("message")
    user = User.objects.get(id=user_id)  # Get the logged-in user instance

    # Save the contact data to the database
    insertquery = Contact(
        user=user,
        name=name,
        email=email,
        phone_number=phone_number,
        msg_subject=msg_subject,
        message=message
    )
    insertquery.save()

    # Get the logged-in user's email
    user = User.objects.get(id=user_id)  # Get the logged-in user
    user_email = user.email  # Get the user's email

    # Prepare the email content
    subject = f"Contact Form Submission: {msg_subject}"
    email_message = (
        f"Dear {name},\n\n"
        "Thank you for reaching out to us! \n"
        "Here is a summary of your submission:\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone Number: {phone_number}\n"
        f"Subject: {msg_subject}\n"
        f"Message: {message}\n"
    
        "We will get back to you shortly.\n\n"
        "Best regards,\n"
        "Medizo"
    )

    # Create and send the email
    email_to_user = EmailMessage(
        subject,
        email_message,
        'your_email@gmail.com',  # Replace with your email
        [user_email],
    )
    email_to_user.send(fail_silently=False)  # Send the email

    messages.success(request, "Message Sent Successfully!")
    return redirect("/contact")


def shop(request):
    fetchdata = Medicine.objects.all()
    fetchcatdata= Subcategory.objects.all()

    # Get the selected category ID from the request
    selected_category_id = request.GET.get('category_id', None)

    # Set up pagination
    paginator = Paginator(fetchdata, 6)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    result_count = medicines.paginator.count

    context = {
        "data": medicines,
        "catdata": fetchcatdata,
        "result_count": result_count,
        "selected_category_id": selected_category_id  # Pass the selected category ID

    }
    return render(request, "shop.html", context)

def catviseproduct(request, id):
    fetchcatdata = Subcategory.objects.all()  # Fetch all subcategories
    try:
        catdata = Subcategory.objects.get(id=id)  # Get the selected subcategory
    except Subcategory.DoesNotExist:
        catdata = None  # Handle the case where the category does not exist

    fetchdata = Medicine.objects.filter(subcategory=id)  # Filter medicines by selected subcategory

    context = {
        "data": fetchdata,
        "catdata": fetchcatdata,  # Pass all subcategories to the context
        "id": catdata.name if catdata else "Not Available",
        "selected_category_id": id  # Pass the selected category ID

    }

    return render(request, "shop.html", context)

def shopdetails(request, id):
    singledata = Medicine.objects.get(id=id)
    # Fetch inquiries related to this medicine
    inquiries = Inquiry.objects.filter(medicine=singledata)
    context = {
        "sdata": singledata,
        "inquiries": inquiries,  # Add inquiries to the context

    }
    return render(request, "shop-details.html", context)

def search(request):
    search_keyword=request.POST.get("keyword")
    print(search_keyword)
    fetchdata=Medicine.objects.filter(Q(name__icontains=search_keyword)| Q(description__icontains=search_keyword))
    context = {
            "data":fetchdata
        }
    return render(request,"shop.html",context)

def appointment(request):
    departments = Department.objects.all()
    doctors = None  # Initialize doctors as None
    selected_department_name = None  # Initialize selected department name

    # Initialize context dictionary
    context = {
        "data1": departments,
        "data2": doctors,
        "selected_department_name": selected_department_name  # Pass the selected department name (if any)
    }

    # Always attempt to get the department ID from the request
    department_id = request.POST.get('department')
    if department_id:
        # Fetch doctors based on the selected department
        doctors = Doctor.objects.filter(department_id=department_id)
        context["data2"] = doctors  # Update doctors in context

        # Get the name of the selected department
        try:
            selected_department = Department.objects.get(id=department_id)
            selected_department_name = selected_department.name
            context["selected_department_name"] = selected_department_name  # Update selected department name in context
        except Department.DoesNotExist:
            context["selected_department_name"] = None  # Handle case where department does not exist

        context["selected_department"] = department_id  # Pass the selected department ID

    return render(request, "appointment.html", context)

def book_appointment(request):
        user_id = request.session["log_id"]
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        name = request.POST.get('name')
        email = request.POST.get('email')
        appointment_time = request.POST.get('appointment_time')
        appointment_date = request.POST.get('appointment_date')

        user = User.objects.get(id=user_id)  # Get the logged-in user instance
        insertquery = Appointment(
            user=user,  # Pass the user instance directly
            department=Department(id=department),
            doctor=Doctor(id=doctor),
            name=name,
            email=email,
            appointment_time=appointment_time,
            appointment_date=appointment_date
        )
        insertquery.save()
        # Get the logged-in user's email
        user = User.objects.get(id=user_id)  # Get the logged-in user
        user_email = user.email  # Get the user's email

        # Retrieve the medicine name using the medicine ID
        department = Department.objects.get(id=department)
        department_name = department.name  # Assuming the Medicine model has a 'name' field

        # Retrieve the medicine name using the medicine ID
        doctor = Doctor.objects.get(id=doctor)
        doctor_name = doctor.name  # Assuming the Medicine model has a 'name' field

        # Send email to the logged-in user
        subject = "Appointment Confirmation"
        message = (
            f"Dear {name},\n\n"
            f"Your appointment has been booked successfully!\n\n"
            f"Department: {department_name}\n"
            f"Doctor: {doctor_name}\n"
            f"Appointment Date: {appointment_date}\n"
            f"Appointment Time: {appointment_time}\n\n"
            "Thank you for choosing our service!\n"
            "Best regards,\n"
            "Medizo"
        )

        send_mail(
            subject,
            message,
            'your_email@gmail.com',  # Replace with your email
            [user_email],  # Send to the logged-in user's email
            fail_silently=False,
        )
        messages.success(request,"Appointment booked successfully! A confirmation email has been sent to your registered email address.")
        return redirect('/appointment')

def services1(request):
    fetchdata = Service.objects.all()

    # Set up pagination
    paginator = Paginator(fetchdata, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "data": page_obj,
    }

    return render(request, "services-1.html", context)

def servicedetails(request,id):
    singledata = Service.objects.get(id=id)
    context = {
        "sdata": singledata
    }
    return render(request,"service-details.html",context)

def doctors(request):
    fetchdoctor=Doctor.objects.all()

    # Set up pagination
    paginator = Paginator(fetchdoctor, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        "data":page_obj
    }
    return render(request,"doctors.html",context)

def doctorsdetails(request,id):
    singledoctor = Doctor.objects.get(id=id)
    context = {
        "ddata": singledoctor
    }
    return render(request,"doctors-details.html",context)

def inquiry(request,id):
    fetchdata=Medicine.objects.get(id=id)
    context={
        "pid":id,
        "sdata":fetchdata
    }
    return render(request,"Inquiry.html",context)

def showinquiries(request):
    user=request.session["log_id"]
    inquiries = Inquiry.objects.filter(user=user).order_by('-created_at')  # Get all inquiries ordered by date
    context={
        "data":inquiries
    }
    return render(request,"showinquiries.html",context)


def inquirydata(request):
    pid = request.POST.get('pid')
    user_id = request.session["log_id"]
    quantity = request.POST.get('quantity')
    phone = request.POST.get('phone')
    number = request.POST.get('number')
    societyname = request.POST.get('societyname')
    landmark = request.POST.get('landmark')
    street = request.POST.get('street')
    city = request.POST.get('city')
    pincode = request.POST.get('pincode')
    message = request.POST.get('message')

    # Create a new inquiry instance
    insertquery = Inquiry(
        user=User(id=user_id),
        medicine=Medicine(id=pid),
        quantity=quantity,
        phone=phone,
        number=number,
        societyname=societyname,
        landmark=landmark,
        street=street,
        city=city,
        pincode=pincode,
        message=message,
    )
    insertquery.save()
    # Retrieve the logged-in user's email
    user = User.objects.get(id=user_id)
    user_email = user.email

    # Retrieve the medicine name using the medicine ID
    medicine = Medicine.objects.get(id=pid)
    medicine_name = medicine.name  # Assuming the Medicine model has a 'name' field

    # Prepare email content using the HTML template
    email_message = render_to_string('inquiry_confirmation_email.html', {
        'user_name': user.name,
        'medicine_name': medicine_name,
        'medicine_id': pid,
        'quantity': quantity,
        'phone': phone,
        'number': number,
        'society_name': societyname,
        'landmark': landmark,
        'street': street,
        'city': city,
        'pincode': pincode,
        'message': message,
    })

    subject = 'Inquiry Confirmation'
    recipient_list = [user_email]  # Send email to the logged-in user

    # Send email
    send_mail(
        subject,
        'This is a fallback message if HTML is not supported.',
        'your_email@gmail.com',  # Replace with your email
        recipient_list,
        fail_silently=False,
        html_message=email_message  # Send as HTML
    )
    messages.success(request, "Inquiry Generated successfully! A confirmation email has been sent.")
    return redirect("/shop")

def fourzerofour(request):
    return render(request,"404.html")

def about(request):
    fetchdoctor = Doctor.objects.all()[:3]
    context = {
        "ddata": fetchdoctor
    }
    return render(request,"about.html",context)

def blog2(request):
    return render(request,"blog-2.html")

def blogdetails(request):
    return render(request,"blog-details.html")

def casedetails(request):
    return render(request,"case-details.html")

def casestudy(request):
    return render(request,"case-study.html")

def checkout(request):
    return render(request,"checkout.html")

def comingsoon(request):
    return render(request,"coming-soon.html")

def departments(request):
    fetchdoctor = Department.objects.all()

    # Set up pagination
    paginator = Paginator(fetchdoctor, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "data": page_obj
    }
    return render(request,"departments.html",context)

def faq(request):
    return render(request,"faq.html")

def hellomedizo(request):
    return render(request,"hello@medizo.html")

def newsdetails(request):
    return render(request,"news-details.html")

def privacypolicy(request):
    return render(request,"privacy-policy.html")

def termscondition(request):
    return render(request,"terms-condition.html")

def testimonials(request):
    return render(request,"testimonials.html")

def forgotpasswordpage(request):
     return render(request,"forgot password.html")

def forgot_password(request):
    email = request.POST.get("email")
    print(email)

    useremail=User.objects.get(email=email)
    print(useremail)

    if useremail is not None:
    # Generate a new password
        letters = string.ascii_letters  # a-zA-Z
        numbers = string.digits  # 0-9
        symbols = '!#$%&()*+'  # Special characters

        nr_letters = 2
        nr_symbols = 1
        nr_numbers = 1


        password_list = []

        for char in range(1,nr_letters+1):
            password_list.append(random.choice(letters))

        for char in range(1,nr_symbols+1):
            password_list += random.choice(symbols)

        for char in range(1,nr_numbers+1):
            password_list+= random.choice(numbers)
        print(password_list)
        random.shuffle(password_list)
        print(password_list)

        password = ""

        for char in password_list:
            password += char

        cuser=User.objects.get(email=email)
        cuser.password=password
        cuser.save(update_fields=['password'])

    # Prepare the email content
    subject = 'Your New Password'
    message = f"""
    Dear User,

    We have received a request to reset the password for your account associated with this email address: {email}.

    Your new password is: {password}

    Please log in using this password and consider changing it to something more memorable after your first login. If you did not request this change, please contact our support team immediately.

    Thank you for your attention.

    Best regards,
       Medizo
    """

    # Send the email
    send_mail(
        subject,
        message,
        'from@example.com',  # Replace with your sender email
        [email],
        fail_silently=True,
    )

    messages.success(request, "Password updated successfully. Please check your email.")
    return redirect("/sign-in")