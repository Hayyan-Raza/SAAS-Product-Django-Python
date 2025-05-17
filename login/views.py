from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import subprocess, json
from login.forms import UserForm, UserProfileForm


def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)  # For image upload support

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)  # Log user in after registering
            return redirect('home')

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'login/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


@login_required
def home(request):
    return render(request, 'login/home.html')


@csrf_exempt
def analyze_website(request):
    print("Analyzing.....")
    report_data = None
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            try:
                subprocess.run([
                    "lighthouse.cmd", url,
                    "--output=json",
                    "--output-path=report.json",
                    "--quiet",
                    "--chrome-flags=--headless"
                ], check=True)
                with open("report.json", "r", encoding="utf-8") as f:
                    report_data = json.load(f)
            except subprocess.CalledProcessError as e:
                report_data = {"error": "Lighthouse analysis failed."}
    return render(request, 'login/home.html', {'report': report_data})
