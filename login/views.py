from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import markdown
from login.forms import UserForm, UserProfileForm
from dotenv import load_dotenv
import os
# from google import genai
import google.generativeai as genai
from django.utils.safestring import mark_safe

load_dotenv()  # Load .env file

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

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
# def generate_resume(request):
#     print("generating resume")
#     generated_cv = None
#     error = None

#     if request.method == 'POST':
#         print("correct method")
#         prompt = request.POST.get('prompt')

#         if prompt:
#             try:
#                 # Initialize the Generative AI client
#                 genai.configure(api_key=GEMINI_API_KEY)
#                 # Generate resume using Gemini
#                 response = genai.generate_content(
#                     model="models/gemini-2.0-flash",
#                     contents=[{"role": "user", "parts": [f"Create a professional resume based on the following details:\n{prompt}"]}]
#                 )

#                 print("coolling")
#                 generated_cv = response.text
#                 print(generated_cv)

#             except Exception as e:
#                 error = f"An error occurred while generating the resume: {str(e)}"
#                 print(error)
#         else:
#             error = "Please enter your details to generate a resume."
#             print(error)

#     return render(request, 'login/home.html', {
#         "generated_cv": generated_cv,
#         "error": error
#     })

def generate_resume(request):
    generated_cv = None
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"Create a professional resume based on the following input: {prompt}"
                )
                generated_cv = markdown.markdown(response.text)

            except Exception as e:
                generated_cv = f"An error occurred while generating the resume: {str(e)}"
    return render(request, "login/home.html", {'html': mark_safe(generated_cv)})