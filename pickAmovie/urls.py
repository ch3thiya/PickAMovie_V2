"""
URL configuration for pickAmovie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# In pickAmovie/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from movies.forms import CustomAuthenticationForm  # Make sure to import your custom form

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Our custom Login URL. This will be found first.
    path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),

    # 2. Our custom Logout URL. This will be found second.
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # 3. The generic auth URLs. This provides other routes like password reset.
    #    Since our login/logout are defined above, this line's login/logout will be ignored.
    path('accounts/', include('django.contrib.auth.urls')),

    # 4. Our main application's URLs.
    path('', include('movies.urls')),
]
