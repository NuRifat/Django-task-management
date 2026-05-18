from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm

# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form":form})