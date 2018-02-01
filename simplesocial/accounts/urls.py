from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        # views.activate, name='activate'),
    url(r'^signup/$', views.signup, name='signup'),
]
