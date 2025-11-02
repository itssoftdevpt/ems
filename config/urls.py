from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/tenant/', include('organizations.urls')),
    path('api/students/', include('students.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/fees/', include('fees.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/calendars/', include('calendars.urls')),
    path('api/reporting/', include('reporting.urls')),
]
