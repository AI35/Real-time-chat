from django.contrib import admin
from django.urls import path, include
from chat.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('chat.urls')),
]
