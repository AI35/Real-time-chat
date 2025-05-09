from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.utils.text import slugify
from django.contrib.auth.views import LoginView
from .models import Room, Message
from .forms import RoomForm, SignUpForm, EmailOrUsernameAuthenticationForm

def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room)[:50]
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })

def logout_view(request):
    logout(request)
    return redirect('chat:index')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat:index')
    else:
        form = SignUpForm()
    return render(request, 'chat/signup.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = EmailOrUsernameAuthenticationForm
    template_name = 'registration/login.html'

@user_passes_test(lambda u: u.is_staff)
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)
            room.save()
            return redirect('chat:index')
    else:
        form = RoomForm()
    
    return render(request, 'chat/create_room.html', {'form': form})