from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', include('messaging.urls')),
    path('login/', LoginView.as_view(template_name='messages/login.html')),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('admin/', admin.site.urls),
    
]