from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})
