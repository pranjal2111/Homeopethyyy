from django.contrib import admin
from .models import *

# Country Admin
#class showCountry(admin.ModelAdmin):
#    list_display = ['id', 'name']
 #   list_filter = ['name']

#admin.site.register(Country, showCountry)

# State Admin
#class showState(admin.ModelAdmin):
 #   list_display = ['id', 'name', 'country']
  #  list_filter = ['country',]
   # search_fields = ['name', 'country']
    #list_editable = ['name', 'country']

#admin.site.register(State, showState)

# City Admin
#class showCity(admin.ModelAdmin):
 #   list_display = ['id', 'name', 'state']
  #  list_filter = ['state']
   # search_fields = ['name', 'state']
  #  list_editable = ['name', 'state']

#admin.site.register(City, showCity)

# User Admin
class showUser(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone_number','password','dp_photo' ,'created_at', 'updated_at','city','state']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'email', 'phone_number']
    list_editable = ['name', 'phone_number']

admin.site.register(User, showUser)


# Category Admin
class showCategory(admin.ModelAdmin):
    list_display = ['id', 'name','description','created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['name', 'description']

admin.site.register(Category, showCategory)

# Subcategory Admin
class showSubcategory(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description' ,'created_at']
    list_filter = ['category', 'name', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['name', 'description', 'category']

admin.site.register(Subcategory, showSubcategory)

# Medicine Admin
class showMedicine(admin.ModelAdmin):
    list_display = ['id', 'name', 'subcategory','description','ingredients','medicine', 'price', 'stock_quantity', 'made_to_order', 'created_at']
    list_filter = ['subcategory', 'price', 'made_to_order', 'created_at']
    search_fields = ['name', 'description', 'ingredients', 'subcategory__name']
    list_editable = ['name', 'price', 'stock_quantity', 'made_to_order']

admin.site.register(Medicine, showMedicine)

# Inquiry Admin
class showInquiry(admin.ModelAdmin):
    list_display = ['id', 'user', 'medicine', 'quantity', 'status','message', 'created_at']
    list_filter = ['user', 'medicine', 'status', 'created_at']
    search_fields = ['user__full_name', 'medicine__name', 'status', 'message']
    list_editable = ['quantity', 'status']

admin.site.register(Inquiry, showInquiry)

# Appointment Admin
class showAppointment(admin.ModelAdmin):
    list_display = ['id', 'name', 'doctor','department','email', 'appointment_time','appointment_date', 'status','notes','created_at']
    list_filter = ['name', 'doctor', 'status', 'created_at']
    search_fields = ['name', 'doctor','appointment_date', 'status', 'notes']
    list_editable = ['appointment_time', 'status']

admin.site.register(Appointment, showAppointment)

class showContact(admin.ModelAdmin):
    list_display = ['id','name','email','phone_number','msg_subject','message']
admin.site.register(Contact,showContact)

class showService(admin.ModelAdmin):
    list_display = ['id','name','desc','services']
admin.site.register(Service,showService)

class showDepartment(admin.ModelAdmin):
    list_display = ['id','name','description']
admin.site.register(Department,showDepartment)

class showDoctor(admin.ModelAdmin):
    list_display = ['id','name','specialist','doctors']
admin.site.register(Doctor,showDoctor)