from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def login(request):
    # 만약 이미 로그인 되어 있는 유저가 GET 요청을 보내면, 돌려보내자.
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
    # return redirect('articles:index')
    return redirect('accounts:login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    if request.method == "POST":
        request.user.delete()
    return redirect('articles:index')


@login_required
def update(reqeust):
    if reqeust.method == 'POST':
        form = CustomUserChangeForm(reqeust.POST, instance=reqeust.user)
        if form.is_valid():
            form.save()
            return redirect('aritlces:index')
    else :
        form = CustomUserChangeForm( instance=reqeust.user )
    context = { 
        'form':form
    }
    return render(reqeust, 'accounts/update.html',context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request, "accounts/password_change.html", context)