from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

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


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/my_account.html'
    fields = ('first_name', 'last_name', 'email',)
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user
