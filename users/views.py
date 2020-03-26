from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            login(request, new_user)
            return redirect('logger:home')
    else:
        register_form = UserCreationForm()
    context = {'register_form':register_form}
    return render(request, 'registration/register.html', context)
