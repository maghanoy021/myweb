from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  # use .get() to avoid MultiValueDictKeyError
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in both fields.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')  # redirect to next page or dashboard
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'main/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {
        'announcements': Announcement.objects.all(),
        'events': Event.objects.all()
    })

@login_required
def announcements(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        return redirect('dashboard')
    return render(request, 'main/announcements.html', {'form': form})

@login_required
def events(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        return redirect('dashboard')
    return render(request, 'main/events.html', {'form': form})

@login_required
def messages_view(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('messages')
    else:
        form = MessageForm()
    inbox = Message.objects.filter(receiver=request.user)
    sent = Message.objects.filter(sender=request.user)
    return render(request, 'main/messages.html', {'form': form, 'inbox': inbox, 'sent': sent})

@login_required
def file_list(request):
    files = File.objects.all()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            return redirect('files')
    else:
        form = FileForm()
    return render(request, 'main/files.html', {'files': files, 'form': form})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        pwd_form = PasswordChangeMiniForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")

        if pwd_form.is_valid() and pwd_form.cleaned_data.get("password1"):
            user.set_password(pwd_form.cleaned_data["password1"])
            user.save()
            messages.success(request, "Password updated. Please login again.")
            return redirect("login")

    else:
        form = ProfileUpdateForm(instance=user)
        pwd_form = PasswordChangeMiniForm()

    return render(request, "main/edit_profile.html", {
        "form": form,
        "pwd_form": pwd_form
    })

@login_required
def profile(request):
    user = request.user

    if user.role == "admin":
        return render(request, "main/admin_profile.html", {
            "user": user,
            "total_users": User.objects.count(),
            "total_announcements": Announcement.objects.count(),
            "total_events": Event.objects.count(),
            "total_files": File.objects.count(),
            "total_messages": Message.objects.count(),
        })

    return render(request, "main/profile.html", {"user": user})
