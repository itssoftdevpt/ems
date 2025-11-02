import os

from django.core.asgi import get_asgi_application
from django_tenants.middleware.main import TenantMainMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = TenantMainMiddleware(get_asgi_application())
