from django.urls import include, path

urlpatterns = [
    path('api/tenancy/', include('tenancy.urls')),
]
