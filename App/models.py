from django.db import models
from django.utils.safestring import mark_safe

STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
STATUS1_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
STATUS2_CHOICES = [
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]
STATUS3_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]

DEPARTMENT_CHOICES = [
        ('Dental Care', 'Dental Care'),
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Medicine', 'Medicine'),
    ]

DOCTOR_CHOICES = [
        ('Dr. James Adult', 'Dr. James Adult'),
        ('Dr. James Alison', 'Dr. James Alison'),
        ('Dr. Peter Adlock', 'Dr. Peter Adlock'),
        ('Dr. Jelin Alis', 'Dr. Jelin Alis'),
        ('Dr. Josh Taylor', 'Dr. Josh Taylor'),
        ('Dr. Steven Smith', 'Dr. Steven Smith'),
    ]

SPECIALIST_CHOICES = [
        ('Cardiologists', 'Cardiologists'),
        ('Dermatologists', 'Dermatologists'),
        ('Endocrinologists', 'Endocrinologists'),
        ('Gastroenterologists', 'Gastroenterologists'),
        ('Allergists', 'Allergists'),
        ('Immunologists', 'Immunologists'),
    ]

# User Model
class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=60)
    user_dp = models.ImageField(upload_to='dp')

    def dp_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.user_dp.url))

    dp_photo.allow_tags = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Subcategory Model
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Medicine Model
class Medicine(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    del_price = models.FloatField(null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='medicine_images')
    def medicine(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    medicine.allow_tags = True
    stock_quantity = models.IntegerField()
    made_to_order = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    Tag=models.CharField(max_length=40,null=True)
    status=models.CharField(max_length=15,null=True,choices=STATUS3_CHOICES)
    def __str__(self):
        return self.name


# Inquiry Model
class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    phone=models.BigIntegerField(null=True)
    number=models.CharField(max_length=5,null=True)
    societyname=models.CharField(max_length=30,null=True)
    landmark=models.CharField(max_length=30,null=True)
    street=models.CharField(max_length=30,null=True)
    city=models.CharField(max_length=30,null=True)
    pincode=models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="Pending")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10)
    msg_subject=models.CharField(max_length=50)
    message=models.TextField()

class Service(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    img=models.ImageField(upload_to='services',null=True)

    def services(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.img.url))

    services.allow_tags = True

class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    img = models.ImageField(upload_to='department', null=True)

    def department(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.img.url))

    department.allow_tags = True

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    specialist = models.CharField(max_length=70)
    img = models.ImageField(upload_to='doctors', null=True)

    def doctors(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.img.url))

    doctors.allow_tags = True

    education=models.CharField(max_length=30,null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    experience=models.CharField(max_length=70,null=True)
    certifications=models.CharField(max_length=100,null=True)
    practicearea=models.CharField(max_length=100,null=True)
    phone=models.BigIntegerField(null=True)
    email=models.EmailField(null=True)
    desc=models.TextField(null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    email = models.EmailField(default=0)
    appointment_time = models.TimeField()
    appointment_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=STATUS1_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


