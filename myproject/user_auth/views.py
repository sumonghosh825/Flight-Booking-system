from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
# Email verification imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


# ================= REGISTER =================
def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            email=email,
            username=username,
            password=password
        )

        user.is_active = False   # 🔴 inactive until email verify
        user.save()

        # EMAIL SEND
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

        

        send_mail(
            'Verify your email',
            f'Click this link:\n{verification_link}',
            settings.EMAIL_HOST_USER,
            [email],
        )
        # return redirect('login_')

        return render(request, 'check_email.html')

    return render(request, 'register.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'verification_success.html')
        else:
            return HttpResponse("Invalid or expired token")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Something went wrong")


# ================= LOGIN =================
def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login_.html', {'error': 'Please verify your email first'})
        else:
            return render(request, 'login_.html', {'error': 'Invalid username or password'})

    return render(request, 'login_.html')



@login_required 
def reset_pass(request):
    if request.method == 'POST':
        oldpass = request.POST.get('old_pass')
        newpass = request.POST.get('new_pass')

        user = authenticate(request, username=request.user.username, password=oldpass)

        if not user:
            return render(request, 'reset_pass.html', {'error': 'Old password is wrong'})

        if user.check_password(newpass):
            return render(request, 'reset_pass.html', {'error': 'New password cannot be same as old password'})

        user.set_password(newpass)
        user.save()

        return redirect('login_')  

    return render(request, 'reset_pass.html')


def forgot_pass(request): 
    if request.method == 'POST': 
        username = request.POST['username'] 
        try: 
            user = User.objects.get(username=username) 
            request.session['fp_user'] = username
            return redirect('new_pass') 
        except User.DoesNotExist: 
            return render(request, 'forgot_pass.html', {'error': 'Username does not exist'}) 

    return render(request, 'forgot_pass.html')



    
def new_pass(request): 
    username = request.session.get('fp_user') 

    if not username:
        return redirect('forgot_pass') 

    user = User.objects.get(username=username)

    if request.method == 'POST': 
        new_pass = request.POST['new_pass'] 

        if user.check_password(new_pass): 
            return render(request, 'new_pass.html', {'error': 'New password should not be same as old password'})

        user.set_password(new_pass) 
        user.save() 

        del request.session['fp_user'] 
        return redirect('login_') 

    return render(request, 'new_pass.html')


# ================= LOGOUT =================
@login_required
def logout_(request):
    logout(request)
    return redirect('login_')


# ================= PROFILE =================
@login_required
def profile(request):
    return render(request, 'profile.html')