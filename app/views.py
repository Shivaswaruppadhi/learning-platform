from django.shortcuts import render,redirect
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import random
# Create your views here.




def passwordValidation(passw):
    cap = 0
    lower = 0
    spe = 0
    num = 0
    for i in passw:
        if i.isupper():
            cap += 1
        elif i.islower():
            lower += 1
        elif i.isdigit():
            num += 1
        else:
            spe += 1
    
    if len(passw) !=10:
        return 'Password must have at exactly 10 letters'
    if cap < 1:
        return 'Password must have at least one uppercase letter'
    if lower < 1:
        return 'Password must have at least one lowercase letter'
    if spe < 1:
        return 'Password must have at least one special character'
    if num < 1:
        return 'Password must have at least one number'




def registration(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    d = {'EUFO':EUFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        NMUFO = UserForm(request.POST)
        NMPFO = ProfileForm(request.POST,request.FILES)
        if NMUFO.is_valid() and NMPFO.is_valid():

            MUFO = NMUFO.save(commit=False)
            pwd = NMUFO.cleaned_data['password']
            new = passwordValidation(pwd)
            if new:
                return HttpResponse(new)
            MUFO.set_password(pwd)
            MUFO.save()

            MPFO = NMPFO.save(commit=False)
            MPFO.username = MUFO
            MPFO.save()

            send_mail('Project Registration',
                    'Thanks For Your Response',
                    'sspadhi03@gmail.com',
                    [MUFO.email],
                    fail_silently=True)

            return HttpResponse('Sucessful')
        else:
            return HttpResponse('Invalid')
        
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        d = {'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['password']
        new = passwordValidation(passw)

        if new:
            return HttpResponse(new)

        AUO = authenticate(username = username,password = passw)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username'] = username
                return HttpResponseRedirect(reverse('home'))
                
            else:
                return HttpResponse('Not active user')
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('home'))


@login_required
def profile_page(request):
    username = request.session.get('username')
    UO = User.objects.get(username=username)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO,'PO':PO}
    return render(request,'profile_page.html',d)


@login_required
def change_password(request):
    if request.method == 'POST':
        pwd = request.POST['pwd']
        rpwd = request.POST['rpwd']
        username = request.session.get('username')

        new = passwordValidation(pwd)
        if new:
            return HttpResponse(new)

        if pwd == rpwd:
            UO = User.objects.get(username=username)
            UO.set_password(pwd)
            UO.save()
            return HttpResponse('Password Changed Successfully')
        else:
            return HttpResponse('The password not matched')
    return render(request,'change_password.html')

def otpgenerator():
    return random.randint(100000,999999)

def otp_page(request):
    if request.method == 'POST':
        otp = request.session.get('otp')
        entered_otp = request.POST['otp']
        if entered_otp and int(entered_otp) == otp:
            return redirect('reset_continuation')
        else:
            return HttpResponse('Invalid OTP')
    return render(request,'otp_page.html')


def reset_password(request):
    if request.method == 'POST':
        user = request.POST['user']
        pwd = request.POST['pwd']
        rpwd = request.POST['rpwd']
        email = request.POST['email']

        new = passwordValidation(pwd)
        if new:
            return HttpResponse(new)
        if pwd == rpwd:
            UO = User.objects.filter(username=user)
            if UO:
                if UO[0].email == email:
                    otp = otpgenerator()
                    request.session['otp'] = otp
                    request.session['username'] = user
                    request.session['password'] = pwd
                    
                    send_mail(
                        'Reset OTP',
                        f'{otp} is need to be typed for reset your password ',
                        'sspadhi03@gmail.com',
                        [email],
                        fail_silently=False
                    )

                    return redirect('otp_page')
                else:
                    return HttpResponse('Email not matched')
            else:
                return HttpResponse('Not a valid user')
        else:
            return HttpResponse('The password not matched')
    return render(request,'reset_password.html')




def reset_continuation(request):
    username = request.session.get('username')
    password = request.session.get('password')
    UO = User.objects.filter(username = username)
    if UO:
        UO[0].set_password(password)
        UO[0].save()
        return HttpResponse('Reset is done after the validation')
    else:
        return HttpResponse('user is not valid')
    

def courseData(request):
    ECF = CourseMF()
    if request.method == 'POST':
        CFDO = CourseMF(request.POST)
        if CFDO.is_valid():
            CFDO.save()
            return render(request,'courseData.html',{'ECF':ECF})
    return render(request,'courseData.html',{'ECF':ECF})

def courses(request):
    items = Course.objects.all()
    return render(request,'courses.html',{'items':items})

def EnrollmentDetails(request):
    EEF = EnrollmentMF()
    if request.method == 'POST':
        EFDO = EnrollmentMF(request.POST)
        if EFDO.is_valid():
            MUN = EFDO.save(commit=False)
            username = EFDO.cleaned_data['username']
            title = EFDO.cleaned_data['title']
            MUN.save()
            return render(request,'interface.html',{'username':username,'items': Course.objects.get(title=title)})
    return render(request,'EnrollmentDetails.html',{'EEF':EEF})
