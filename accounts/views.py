from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from . import forms
from .forms import MyUserCreationForm, ProfileEditForm
from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from .forms import UserEditForm, ProfileEditForm
# Create your views here.
def home(request):
    return render(request,'home.html')

def profile(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Saved Successfully')
    return render(request,'dashboard/profile.html',{'user_form': user_form, 'profile_form': profile_form})

def about(request):
    return render(request,'about.html')

def staff(request):
    return render(request,'staff.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        contact = Contact(name=name,  email=email, phone=phone, message=message)
        contact.save()

        messages.success(request,'Your message was sent successfully we will get back to you shortly')
    return render(request,'contact.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('profile')  # Redirect to the edit view after successful login
        else:
            messages.info(request, 'Username OR password is incorrect')
    
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/account_settings/')
    else:
        form = MyUserCreationForm()
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user=form.save()
                
                # Check if the profile already exists
                if not hasattr(user, 'profile'):
                    # Create the user profile
                    profile = Profile.objects.create(user=user)
                
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account Created Successfully')
                return redirect('/login/')
            else:
                messages.error(request, 'Error creating account')
        
        context={'form':form}
    return render(request,'register.html',context)



def edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Saved Successfully')


    return render(request, 'dashboard/account_settings.html', {'user_form': user_form, 'profile_form': profile_form})

def initiate_payment(request: HttpRequest) -> HttpResponse:
    school_fee=SchoolFees.objects.all()
    if request.method == 'POST':
        payment_form=forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            
            payment=payment_form.save()
            return render(request,'dashboard/makepayment.html',{'payment':payment,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form=forms.PaymentForm()
    return render(request,'dashboard/fees.html',{'payment_form':payment_form,'school_fee':school_fee})

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    return render(request,'dashboard/success.html')

def history(request):
    pick = Payment.objects.order_by('-created_at').filter(user_id=request.user.id)
    context = {'pick': pick}
    return render(request,'dashboard/history.html',context)

def detail(request,pk):
    pick = Payment.objects.get(pk=pk)
    context={'pick':pick}
    return render(request,'dashboard/detail.html',context)