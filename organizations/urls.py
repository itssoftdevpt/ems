from django.urls import path

from organizations.views import ModuleToggleView, SchoolProfileView, TenantBrandingView

urlpatterns = [
    path('profile/', SchoolProfileView.as_view(), name='school-profile'),
    path('branding/', TenantBrandingView.as_view(), name='tenant-branding'),
    path('modules/', ModuleToggleView.as_view(), name='module-toggles'),
]
