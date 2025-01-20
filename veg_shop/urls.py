from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from cart import views as cart_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('cart.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        next_page='home'
    ), name='login'),
#    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
#    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html', 
#                                                         next_page='/'), name='logout'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='registration/logout.html',
        next_page='/',
        http_method_names=['post', 'get']
    ), name='logout'),


    path('accounts/register/', cart_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
