from .forms import UserCreateForm
from django.shortcuts import render, redirect
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return render(request, 'accounts/signup_complete.html')
    else:
        form = UserCreateForm()

    return render(request, 'accounts/signup.html', {'form': form})


from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = UserModel.objects.get(**kwargs)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None