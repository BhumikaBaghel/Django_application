from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm
from .forms import SignupForm
from django.contrib.auth.models import User
from core.models import Profile  # Replace 'myapp' with your app name

def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})
@login_required
def profile(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        username = request.user.username
        print(f"Username: {username}")
    else:
        print("User is not authenticated")

    return render(request, 'core/profile.html', {'username': username})


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page after updating the picture
    else:
        form = ProfilePictureForm()

    return render(request, 'core/update_profile_picture.html', {'form': form})


@login_required
def delete_user_profile(request, username):
    from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

@login_required
def delete_user_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user.delete()
            return redirect('')  # Redirect to a success page or URL
        except User.DoesNotExist:
            # Handle the case when the user doesn't exist
            return redirect('user_not_found_url')

    return render(request, '')

