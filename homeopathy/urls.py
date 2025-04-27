"""
URL configuration for homeopathy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('forgotpasswordpage', views.forgotpasswordpage),
    path('forgotpassword', views.forgot_password),
    path('404', views.fourzerofour),
    path('about', views.about),
    path('catviseproduct/<int:id>', views.catviseproduct),
    path('appointment', views.appointment),
    path('book_appointment',views.book_appointment),
    path('blog-2', views.blog2),
    path('blog-details', views.blogdetails),
    path('case-details', views.casedetails),
    path('case-study', views.casestudy),
    path('checkout', views.checkout),
    path('coming-soon', views.comingsoon),
    path('contact', views.contact),
    path('contactdata',views.contactdata),
    path('departments', views.departments),
    path('doctors', views.doctors),
    path('doctors-details/<int:id>', views.doctorsdetails),
    path('inquiry/<int:id>', views.inquiry),
    path('showinquiries',views.showinquiries),
    path('inquirydata', views.inquirydata),
    path('faq', views.faq),
    path('hello@medizo', views.hellomedizo),
    path('news-details', views.newsdetails),
    path('privacy-policy', views.privacypolicy),
    path('servicedetails/<int:id>', views.servicedetails),
    path('services-1', views.services1),
    path('shop', views.shop),
    path('shopdetails/<int:id>', views.shopdetails),
    path('sign-in', views.signin),
    path('signindata', views.signindata),
    path('sign-up', views.signup),
    path('signupdata', views.signupdata),
    path('signout',views.signout),
    path('terms-condition', views.termscondition),
    path('testimonials', views.testimonials),
    path('search', views.search),
              ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)